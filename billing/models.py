from django.db import models


# Create your models here.
from patient_report.models import HeaderPatient


class PatientBillHistory(models.Model):
    header_patient = models.ForeignKey(HeaderPatient, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=1000)
    qty = models.CharField(max_length=1000)
    price = models.CharField(max_length=1000)
    patient = models.IntegerField()
    hospital = models.IntegerField()
    doctor = models.IntegerField()
    grand_total = models.IntegerField()

    cash = models.IntegerField(default=0)
    online = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        db_table = 'Patient_bill_history'
