from django.db import models

from appointment.models import PatientAppointment
from store.models import Medicine


class HeaderPatient(models.Model):
    head_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(PatientAppointment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.appointment.patient.user.full_name)


class DetailsPatient(models.Model):
    detail_id = models.AutoField(primary_key=True)
    header = models.ForeignKey(HeaderPatient, on_delete=models.CASCADE)
    medicine_details = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=50, null=True, blank=True, default=None)
    frequency = models.CharField(max_length=50, null=True, blank=True, default=None)
    created_date = models.DateField(null=True, blank=True)
    created_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.header.appointment.patient.user.full_name)
