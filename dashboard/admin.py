from django.contrib import admin
from .models import HospitalAppointmentVisit


# Register your models here.
class HospitalAppointmentVisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'created_at']


admin.site.register(HospitalAppointmentVisit, HospitalAppointmentVisitAdmin)
