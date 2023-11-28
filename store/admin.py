from django.contrib import admin
from .models import Medicine, MainStoreMedicine, MiniStoreMedicine, MedicineTransferHistory


# Register your models here.
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['batch_no', 'name', 'price', 'expiration', 'manufacturer', 'main_store']


class MainStoreMedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'qty', 'from_mini_store', 'to_main_store', 'hospital', 'created_at']


class MiniStoreMedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'qty', 'from_store', 'to_store', 'hospital', 'created_at']


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'qty', 'from_store', 'to_store', 'hospital', 'created_at']


admin.site.register(Medicine, MedicineAdmin)
admin.site.register(MainStoreMedicine, MainStoreMedicineAdmin)
admin.site.register(MiniStoreMedicine, MiniStoreMedicineAdmin)
admin.site.register(MedicineTransferHistory, HistoryAdmin)
