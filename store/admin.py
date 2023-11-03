from django.contrib import admin
from .models import MiniStore, MainStore, Medicine, MappingMedicine, MappingMiniStorMedicine, \
    MainMedicalStoreMedicineTransactionHistory


# Register your models here.
class MainStoreAdmin(admin.ModelAdmin):
    list_display = ['main_store_id', 'main_store_user', 'hospital']


class MiniStoreAdmin(admin.ModelAdmin):
    list_display = ['mini_store_id', 'mini_store_user', 'hospital']


class MedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine_id', 'name', 'description', 'price', 'expiration', 'manufacturer', 'hospital']


class MappingMedicineAdmin(admin.ModelAdmin):
    list_display = ['mapping_id', 'main_qty', 'medicine', 'main_store_user', ]


class MappingMiniStorMedicineAdmin(admin.ModelAdmin):
    list_display = ['mapping_id', 'mini_qty', 'medicine', 'mini_store_user', ]


admin.site.register(MainStore, MainStoreAdmin)
admin.site.register(MiniStore, MiniStoreAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(MappingMedicine, MappingMedicineAdmin)
admin.site.register(MappingMiniStorMedicine, MappingMiniStorMedicineAdmin)
admin.site.register(MainMedicalStoreMedicineTransactionHistory)
