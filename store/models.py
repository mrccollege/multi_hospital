from accounts.models import CustomUser, HospitalUser
from django.db import models


class MainStore(models.Model):
    main_store_id = models.AutoField(primary_key=True)
    main_store_user = models.ForeignKey(CustomUser, related_name='main_store_user', on_delete=models.CASCADE)
    hospital_user = models.ForeignKey(HospitalUser, related_name='main_hospital_user', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.main_store_user.username)

    class Meta:
        db_table = 'main_store'


class MiniStore(models.Model):
    main_store_id = models.AutoField(primary_key=True)
    mini_store_user = models.ForeignKey(CustomUser, related_name='mini_store_user', on_delete=models.CASCADE)
    hospital_user = models.ForeignKey(HospitalUser, related_name='mini_hospital_user', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mini_store_user.username)

    class Meta:
        db_table = 'mini_store'


class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'medicine'


class MappingMedicine(models.Model):
    mapping_id = models.AutoField(primary_key=True)
    main_qty = models.IntegerField()
    price = models.IntegerField()
    expiration = models.DateField()
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    medicine = models.ForeignKey(Medicine, related_name='mapping_medicine', on_delete=models.CASCADE)
    main_store_user = models.ForeignKey(MainStore, related_name='mapping_main_store_user', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'mapping_medicine'


class MappingMiniStorMedicine(models.Model):
    mapping_id = models.AutoField(primary_key=True)
    mini_qty = models.IntegerField()
    medicine = models.ForeignKey(MappingMedicine, related_name='mapping_mini_store_medicine', on_delete=models.CASCADE)
    mini_store_user = models.ForeignKey(CustomUser, related_name='mapping_mini_store_user', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.medicine.medicine.name)

    class Meta:
        db_table = 'mapping_mini_store_medicine'


class MedicineTransactionHistory(models.Model):
    medicine_trans_id = models.AutoField(primary_key=True)
    main_store_medicine_trans = models.ForeignKey(MappingMedicine, related_name='main_store_medicine_trans',
                                                  on_delete=models.CASCADE)
    trans_main_qty = models.IntegerField(default=0)
    mini_store_medicine_trans = models.ForeignKey(MappingMiniStorMedicine, related_name='mini_store_medicine_trans',
                                                  on_delete=models.CASCADE)
    trans_mini_qty = models.IntegerField(default=0)
    trans_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.trans_date)
