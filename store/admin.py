from django.contrib import admin
from .models import MiniStore, MainStore, Medicine, MappingMedicine, MappingMiniStorMedicine, MedicineTransactionHistory

# Register your models here.
admin.site.register(MainStore)
admin.site.register(MiniStore)
admin.site.register(Medicine)
admin.site.register(MappingMedicine)
admin.site.register(MappingMiniStorMedicine)
admin.site.register(MedicineTransactionHistory)
