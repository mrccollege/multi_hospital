from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=500)
    username = models.CharField(max_length=50, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True, default=None)
    password = models.CharField(max_length=16)
    address = models.TextField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, default=None)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    user_type = models.CharField(max_length=10)
    specialization = models.CharField(max_length=100, null=True, blank=True, default=None)
    degree = models.CharField(max_length=500, null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return str(self.username)


class SocialMediaReference(models.Model):
    type_reference = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.type_reference

    class Meta:
        db_table = 'social_media_reference'


class OtherReference(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'other_reference'


class HospitalUser(models.Model):
    h_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class DoctorUser(models.Model):
    d_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class PatientUser(models.Model):
    p_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    social_ref = models.ForeignKey(SocialMediaReference, on_delete=models.CASCADE, default=None)
    other_ref = models.ForeignKey(OtherReference, on_delete=models.CASCADE, default=None)
    patient_ref = models.IntegerField(null=True, default=None)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
