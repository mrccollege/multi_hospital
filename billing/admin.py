from django.contrib import admin
from .models import PatientBillHistory, PatientBillHistoryHead, PatientBillHistoryDetails

# Register your models here.\

admin.site.register(PatientBillHistory)
admin.site.register(PatientBillHistoryHead)
admin.site.register(PatientBillHistoryDetails)
