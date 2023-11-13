from django.db import models

# Create your models here.
from accounts.models import HospitalUser


class HospitalAppointmentVisit(models.Model):
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    price = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'hospital_Appointment_visit'
