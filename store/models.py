from django.db import models

# Create your models here.
from accounts.models import Stores, HospitalUser


class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    batch_no = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    expiration = models.DateField(null=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    main_store = models.ForeignKey(Stores, related_name='Medicine_main_store', on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, related_name='Medicine_hospital', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'medicine'


class MainStoreMedicine(models.Model):
    main_pro_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, related_name='MainStoreMedicine_medicine', on_delete=models.CASCADE)
    qty = models.IntegerField(null=True, default=0)
    from_mini_store = models.ForeignKey(Stores, related_name='MainStoreMedicine_from_mini_store',
                                        on_delete=models.CASCADE, null=True)
    to_main_store = models.ForeignKey(Stores, related_name='MainStoreMedicine_to_main_store', on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, related_name='MainStoreMedicine_hospital', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'main_store_medicine'


class MiniStoreMedicine(models.Model):
    mini_pro_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, related_name='MiniStoreMedicine_medicine', on_delete=models.CASCADE)
    qty = models.IntegerField(null=True)
    from_store = models.ForeignKey(Stores, related_name='MiniStoreMedicine_from_store', on_delete=models.CASCADE)
    to_store = models.ForeignKey(Stores, related_name='MiniStoreMedicine_to_store', on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, related_name='MiniStoreMedicine_hospital', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'mini_store_medicine'


class MedicineTransferHistory(models.Model):
    trans_pro_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, related_name='MedicineTransferHistory_medicine', on_delete=models.CASCADE)
    qty = models.IntegerField(null=True)
    from_store = models.ForeignKey(Stores, related_name='MedicineTransferHistory_from_store', on_delete=models.CASCADE)
    to_store = models.ForeignKey(Stores, related_name='MedicineTransferHistory_to_store', on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, related_name='MedicineTransferHistory_hospital',
                                 on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'medicine_transfer_history'
