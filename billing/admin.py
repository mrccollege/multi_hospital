from django.contrib import admin
from .models import PatientBillHistoryHead, PatientBillHistoryDetails

# Register your models here.
admin.site.register(PatientBillHistoryHead)
admin.site.register(PatientBillHistoryDetails)
