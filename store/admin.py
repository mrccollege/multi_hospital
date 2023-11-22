from django.contrib import admin
from .models import MiniStore, MainStore, Medicine, MappingMiniStorMedicine, \
    MainMedicalStoreMedicineTransactionHistory, MiniMedicalStoreMedicineTransactionHistory, TransferMedicine


# Register your models here.
class TransferMedicineAdmin(admin.ModelAdmin):
    list_display = ['mapping_id', 'qty', 'medicine', 'from_main_store', 'from_mini_store', 'to_main_store',
                    'to_mini_store', 'hospital']


class MainStoreAdmin(admin.ModelAdmin):
    list_display = ['main_store_id', 'main_store_user', 'hospital']


class MiniStoreAdmin(admin.ModelAdmin):
    list_display = ['mini_store_id', 'mini_store_user', 'hospital']


class MedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine_id', 'name', 'description', 'price', 'expiration', 'manufacturer', 'main_store']


class MappingMiniStorMedicineAdmin(admin.ModelAdmin):
    list_display = ['mapping_id', 'mini_qty', 'medicine', 'mini_store_user', ]


admin.site.register(TransferMedicine, TransferMedicineAdmin)
admin.site.register(MainStore, MainStoreAdmin)
admin.site.register(MiniStore, MiniStoreAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(MappingMiniStorMedicine, MappingMiniStorMedicineAdmin)
admin.site.register(MainMedicalStoreMedicineTransactionHistory)
admin.site.register(MiniMedicalStoreMedicineTransactionHistory)
