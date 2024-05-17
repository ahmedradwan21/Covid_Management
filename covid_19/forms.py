from django.contrib.auth import forms as auth_forms
from django import forms
from django.forms.fields import EmailField
from django.forms.widgets import EmailInput, PasswordInput
from .models import *

class PasswordResetForm(auth_forms.PasswordResetForm):
    email  = forms.EmailField(widget=forms.EmailInput(attrs={'class':"form-control"}))



class PasswordResetConfirmForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control'}), label='New password')
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control'}), label='Confirm new password')
    
    
    
class RiskCalculatorForm(forms.ModelForm):
    class Meta:
        model = RiskCalculatorData
        fields = '__all__' 
        exclude = ['user'] 
        
        
        

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})



class CommitForm(forms.ModelForm):
    class Meta:
        model = Commit
        fields = ['commit', 'rating']
        widgets = {
            'commit': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment...'}),
            'rating': forms.Select(choices=[(5, '★★★★★'), (4, '★★★★☆'), (3, '★★★☆☆'), (2, '★★☆☆☆'), (1, '★☆☆☆☆')]),
        }

class DoctorFeedbackForm(forms.ModelForm):
    class Meta:
        model = DoctorFeedback
        fields = ['feedback']