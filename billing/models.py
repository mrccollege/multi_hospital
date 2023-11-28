from django.db import models

# Create your models here.
from accounts.models import PatientUser, DoctorUser, HospitalUser, Stores
from patient_report.models import HeaderPatient
from store.models import Medicine


class PatientBillHistoryHead(models.Model):
    head_id = models.AutoField(primary_key=True)
    header_patient = models.ForeignKey(HeaderPatient, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE, null=True, blank=True)
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    cash = models.IntegerField(null=True, default=0)
    online = models.IntegerField(null=True, default=0)
    remaining = models.IntegerField(null=True, default=0)
    grand_total = models.IntegerField()
    mini_store = models.ForeignKey(Stores, related_name='PatientBillHistoryHead_mini_store', on_delete=models.CASCADE, null=True, blank=True)
    main_store = models.ForeignKey(Stores, related_name='PatientBillHistoryHead_main_store', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        db_table = 'patient_bill_history_head'

    def __str__(self):
        return str(self.hospital)


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
