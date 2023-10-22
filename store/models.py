from django.db import models

from accounts.models import CustomUser, HospitalUser


class MainMedicalStore(models.Model):
    main_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'main_medical_store'


class MiniMedicalStore(models.Model):
    mini_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mini_medical_store'


class Medicine(models.Model):
    main_medicine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()

    main_store = models.ForeignKey(MainMedicalStore, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'medicine'


class MiniStoreMedicine(models.Model):
    mini_medicine_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    mini_store = models.ForeignKey(MiniMedicalStore, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mini_store_medicine'
