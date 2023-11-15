from django.db import models

# Create your models here.
from accounts.models import PatientUser, DoctorUser, HospitalUser
from patient_report.models import HeaderPatient
from store.models import Medicine, MiniStore


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


class PatientBillHistoryHead(models.Model):
    head_id = models.AutoField(primary_key=True)
    header_patient = models.ForeignKey(HeaderPatient, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    cash = models.IntegerField(null=True, default=0)
    online = models.IntegerField(null=True, default=0)
    remaining = models.IntegerField(null=True, default=0)
    grand_total = models.IntegerField()
    mini_store = models.ForeignKey(MiniStore, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        db_table = 'patient_bill_history_head'

    def __str__(self):
        return str(self.patient.user.full_name)


class PatientBillHistoryDetails(models.Model):
    detail_id = models.AutoField(primary_key=True)
    head = models.ForeignKey(PatientBillHistoryHead, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.IntegerField(null=True, blank=True, default=0)
    total = models.IntegerField(null=True, blank=True, default=0)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        db_table = 'patient_bill_history_details'

    def __str__(self):
        return str(self.medicine.name)
