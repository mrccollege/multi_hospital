from django.db import models


# Create your models here.
from accounts.models import HospitalUser, DoctorUser, PatientUser


class PatientAppointment(models.Model):
    patient_appoint_id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE)
    bloodPressure = models.CharField(max_length=10, null=True, blank=True)
    weight = models.CharField(max_length=10, null=True, blank=True)
    appointment_date = models.DateField(default=None)
    appointment_time = models.TimeField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'patient_appointment'

    def __str__(self):
        return str(self.patient)
