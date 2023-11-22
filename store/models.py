from accounts.models import CustomUser, HospitalUser
from django.db import models


class MainStore(models.Model):
    main_store_id = models.AutoField(primary_key=True)
    main_store_user = models.ForeignKey(CustomUser, related_name='main_store_user', on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, related_name='main_hospital_user', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.main_store_user.username)

    class Meta:
        db_table = 'main_store'


class MiniStore(models.Model):
    mini_store_id = models.AutoField(primary_key=True)
    mini_store_user = models.ForeignKey(CustomUser, related_name='mini_store_user', on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, related_name='mini_hospital_user', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mini_store_user.username)

    class Meta:
        db_table = 'mini_store'


class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    batch_no = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    qty = models.IntegerField()
    expiration = models.DateField()
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    main_store = models.ForeignKey(MainStore, related_name='mapping_main_store_user', on_delete=models.CASCADE)

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'main_store_medicine'


class MainMedicalStoreMedicineTransactionHistory(models.Model):
    medicine_trans_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    main_store = models.ForeignKey(MainStore, related_name='main_trans_main_store_user', on_delete=models.CASCADE)
    trans_qty = models.IntegerField()
    trans_created = models.DateField(auto_now_add=True)
    trans_update = models.DateField(null=True)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'main_store_medicine_transaction_history'


class MappingMiniStorMedicine(models.Model):
    mapping_id = models.AutoField(primary_key=True)
    mini_qty = models.IntegerField()
    medicine = models.ForeignKey(Medicine, related_name='mapping_mini_store_medicine', on_delete=models.CASCADE)
    mini_store_user = models.ForeignKey(MiniStore, related_name='mapping_mini_store_user', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'mapping_mini_store_medicine'


class MiniMedicalStoreMedicineTransactionHistory(models.Model):
    medicine_trans_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    main_store = models.ForeignKey(MainStore, related_name='mini_trans_main_store_user', on_delete=models.CASCADE,
                                   null=True, blank=True)
    mini_store = models.ForeignKey(MiniStore, related_name='mini_trans_mini_store_user', on_delete=models.CASCADE,
                                   null=True, blank=True)
    trans_qty = models.IntegerField()
    trans_created = models.DateField(auto_now_add=True)
    trans_update = models.DateField(null=True)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'mini_store_medicine_transaction_history'


class TransferMedicine(models.Model):
    mapping_id = models.AutoField(primary_key=True)
    qty = models.IntegerField()
    medicine = models.ForeignKey(Medicine, related_name='mapping_medicine', on_delete=models.CASCADE)
    from_main_store = models.ForeignKey(MainStore, related_name='from_main_store', on_delete=models.CASCADE, null=True)
    from_mini_store = models.ForeignKey(MiniStore, related_name='from_mini_store', on_delete=models.CASCADE, null=True)
    to_main_store = models.ForeignKey(MainStore, related_name='to_main_store', on_delete=models.CASCADE, null=True)
    to_mini_store = models.ForeignKey(MiniStore, related_name='to_mini_store', on_delete=models.CASCADE, null=True)
    hospital = models.ForeignKey(HospitalUser, related_name='mapping_hospital', on_delete=models.CASCADE)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'transfer_medicine'
