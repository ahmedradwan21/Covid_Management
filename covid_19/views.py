from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import PasswordResetConfirmForm, PasswordResetForm 
from django.contrib.auth import views
from .forms import RiskCalculatorForm, ImageForm
from django.contrib.auth.decorators import login_required
from django.views import View
import uuid
from django.core.mail import send_mail


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


def all_users_view(request):
    if request.user.profile.is_doctor:
        users = User.objects.exclude(profile__is_doctor=True)
    else:
        users = User.objects.filter(profile__is_doctor=False)
    return render(request, 'doctor_page.html', {'users': users})

def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(Profile, user=user)
    image_url = user_profile.profile_image
    risk_data = user_profile.risk_calculator_data
    context = {
        'user_profile': user_profile,
        'image_url': image_url,
        'risk_data': risk_data,
    }

    return render(request, 'patientprofile.html', context)


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




def image_display(request):
    images = Images.objects.filter(user=request.user)
    return render(request, 'image_display.html', {'images': images})



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
    
    
    

def send_email_validation(email, token):
    subject = 'verified Your Account'
    message = f'Hi, paste the link to verify your account 🧾: http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)



def error_page(request):
    return  render(request , 'error.html')

def success(request):
    return render(request , 'success.html')

def token_send(request):
    return render(request , 'token_send.html')



