# from .forms import FeedbackForm
import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import logout


@login_required
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        is_doctor = request.POST.get('is_doctor') == 'on' 

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('/register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('/register')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(user=user, auth_token=auth_token, is_doctor=is_doctor)
        profile_obj.save()
        send_email_validation(email, auth_token)
        messages.success(request, 'Account created successfully.')
        return redirect('/token')
    return render(request, 'register.html')

@login_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            profile = Profile.objects.filter(user=user).first()
            if profile is None or not profile.is_verified:  
                messages.error(request, 'Profile is not verified. Check your email.')
                return redirect('login')

            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login') 

    return render(request, 'login.html')

@login_required
def home(request):
    user_profile = request.user.profile
    existing_image = Images.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect('image_display')  
    else:
        form = ImageForm()
        return render(request, 'home.html')

    if existing_image:
        return redirect('image_update', image_id=existing_image.pk)

    context = {
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'home.html', context)

@login_required
def all_users_view(request):
    if request.user.profile.is_doctor:
        users = User.objects.exclude(profile__is_doctor=True)
    else:
        users = User.objects.filter(profile__is_doctor=False)
    return render(request, 'doctor_page.html', {'users': users})


@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(Profile, user=user)
    image_url = user_profile.profile_image
    risk_data = user_profile.risk_calculator_data
    feedback_form = DoctorFeedbackForm()
    feedbacks = DoctorFeedback.objects.filter(patient=user)

    if request.method == 'POST':
        feedback_form = DoctorFeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.doctor = request.user
            feedback.patient = user
            feedback.save()
            messages.success(request, 'Feedback submitted successfully.')
            return redirect('profile', user_id=user_id)

    context = {
        'user_profile': user_profile,
        'image_url': image_url,
        'risk_data': risk_data,
        'user_id': user_id,
        'feedback_form': feedback_form,
        'feedbacks': feedbacks,
    }
    return render(request, 'patientprofile.html', context)

@login_required
def save_patient_report(request, user_id):
    if request.method == 'POST':
        patient_profile = get_object_or_404(Profile, user__id=user_id)
        patient_profile.patient_report = request.POST.get('patient_report')
        patient_profile.save()
        messages.success(request, 'Patient report saved successfully.')
    return redirect('profile', user_id=user_id)


@login_required
def calculate_risk(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to perform this action.')
        return redirect('login')

    existing_calculation = RiskCalculatorData.objects.filter(user=request.user).first()
    if existing_calculation:
        return redirect('update_calculation', pk=existing_calculation.pk)

    if request.method == 'POST':
        form = RiskCalculatorForm(request.POST)
        if form.is_valid():
            risk_data = form.save(commit=False)
            risk_data.user = request.user
            risk_data.save()

            profile, _ = Profile.objects.get_or_create(user=request.user)
            if not profile.risk_calculator_data:
                profile.risk_calculator_data = risk_data
                profile.save()
                messages.success(request, 'Risk calculator data saved successfully.')
            else:
                messages.warning(request, 'Risk calculator data already exists in your profile.')

            return redirect('success_page', pk=risk_data.pk)
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = RiskCalculatorForm()

    return render(request, 'calculator.html', {'form': form})

@login_required
def update_calculation(request, pk):
    existing_calculation = RiskCalculatorData.objects.filter(pk=pk, user=request.user).first()
    if not existing_calculation:
        messages.error(request, 'No existing calculation found.')
        return redirect('calculate_risk')

    if request.method == 'POST':
        form = RiskCalculatorForm(request.POST, instance=existing_calculation)
        if form.is_valid():
            form.save()
            return redirect('success_page', pk=pk)
    else:
        form = RiskCalculatorForm(instance=existing_calculation)

    return render(request, 'update_calculation.html', {'form': form})




@login_required
def image_upload(request):
    existing_image = Images.objects.filter(user=request.user).first()
    if existing_image:
        return redirect('image_update', image_id=existing_image.pk)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            profile, created = Profile.objects.get_or_create(user=request.user)
            if not profile.profile_image:
                profile.profile_image = image
                profile.save()
            return redirect('profile', user_id=request.user.pk)
    else:
        form = ImageForm()

    return render(request, 'image_upload.html', {'form': form})



@login_required
def image_display(request):
    images = Images.objects.filter(user=request.user)
    return render(request, 'image_display.html', {'images': images})


@login_required
def image_update(request, image_id):
    image = Images.objects.filter(user=request.user, pk=image_id).first()
    if not image:
        return redirect('image_upload')
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('image_display')
    else:
        form = ImageForm(instance=image)
    return render(request, 'image_update.html', {'form': form})


@login_required
def success_page(request, pk):
    risk_data = RiskCalculatorData.objects.filter(pk=pk, user=request.user).first()
    return render(request, 'success_page.html', {'risk_data': risk_data})

class PasswordResetView(views.PasswordResetView):
    template_name = 'account/auth/password_reset.html'
    form_class = PasswordResetForm
    email_template_name = 'account/auth/includes/password_reset_email.html'
    subject_template_name = 'account/auth/includes/password_reset_subject.txt'

class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'account/auth/password_reset_confirm.html'
    form_class = PasswordResetConfirmForm

class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'account/auth/password_reset_done.html'

class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'account/auth/password_reset_complete.html'
    
@login_required
def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
            else:
                profile_obj.is_verified = True
                profile_obj.save()
                messages.success(request, 'Your account has been verified.')
        else:
            messages.error(request, 'Invalid verification token.')
    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred during verification.')

    return redirect('login') 
    
    
    
@login_required
def send_email_validation(email, token):
    subject = 'verified Your Account'
    message = f'Hi, paste the link to verify your account 🧾: http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

@login_required
def error_page(request):
    return render(request, 'error.html')
@login_required
def success(request):
    return render(request, 'success.html')
@login_required
def token_send(request):
    return render(request, 'token_send.html')




# def submit_feedback(request, user_id):
#     if request.method == 'POST':
#         # Process the feedback form data here
#         return redirect('user_profile', user_id=user_id)  # Redirect to user profile or any other page
#     else:
#         # Handle GET request or invalid method
#         return redirect('home')


@login_required
def add_commit(request):
    if request.method == 'POST':
        form = CommitForm(request.POST)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.user = request.user
            commit.save()
            messages.success(request, 'Commit submitted successfully.')
            return redirect('view_commits')
    else:
        form = CommitForm()

    return render(request, 'submit_commit.html', {'form': form})

def view_commits(request):
    if request.method == 'POST':
        form = CommitForm(request.POST)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.user = request.user
            commit.save()
            messages.success(request, 'Commit submitted successfully.')
            return redirect('view_commits')
    else:
        form = CommitForm()

    commits = Commit.objects.all().order_by('-id')  # Display latest commits first
    context = {
        'form': form,
        'commits': commits,
    }
    return render(request, 'view_commit.html', context)

# def logout_view(request):
#     logout(request)
#     return redirect('home')