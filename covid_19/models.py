from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from datetime import datetime


#  feedback for user and doctor can write feedback   (done)
#  imporve design for feedback                       (done)
#  imporve design for register in one block          (done)
#  imporve design for connect with js                (done)
#  commit like feedback with write model and  views  ()
#  page feedback for user can write commit and with page user can see all users commits    ()


class RiskCalculatorData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField()
    cholesterol = models.IntegerField()
    blood_pressure = models.IntegerField()
    hdl_cholesterol = models.IntegerField()
    physical_activity_hours = models.DecimalField(max_digits=5, decimal_places=2)
    alcohol_consumption_per_week = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    smoker = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    family_history_heart_disease = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"RiskCalculatorData - ID: {self.pk}, User: {self.user}"


class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    risk_calculator_data = models.ForeignKey(RiskCalculatorData, on_delete=models.SET_NULL, null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    profile_image = models.OneToOneField(Images, on_delete=models.SET_NULL, null=True, blank=True)
    doctor_report = models.TextField(blank=True)  # Doctor's report
    patient_report = models.TextField(blank=True)
    def __str__(self):
        return self.user.username
    


class DoctorFeedback(models.Model):
    doctor = models.ForeignKey(User, related_name='doctor_feedback', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='patient_feedback', on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.doctor.username} to {self.patient.username}"


class Commit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commit = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Commit by {self.user.username} - {self.commit[:20]}..."