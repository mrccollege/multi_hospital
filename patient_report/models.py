from django.db import models

# Create your models here.
from appointment.models import PatientAppointment
from store.models import Medicine


class HeaderPatient(models.Model):
    head_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(PatientAppointment, on_delete=models.CASCADE)
    disease = models.TextField(null=True, blank=True)
    doctor_status = models.CharField(max_length=10, default='unchecked')
    bill_status = models.CharField(max_length=10, default='unbilled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.appointment.patient.user.full_name)

    class Meta:
        db_table = 'header_patient'


class DetailsPatient(models.Model):
    detail_id = models.AutoField(primary_key=True)
    header = models.ForeignKey(HeaderPatient, on_delete=models.CASCADE)
    medicine_details = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=50, null=True, blank=True, default=None)
    frequency = models.CharField(max_length=50, null=True, blank=True, default=None)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return str(self.header.appointment.patient.user.full_name)

    class Meta:
        db_table = 'details_patient'
