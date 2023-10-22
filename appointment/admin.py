from django.contrib import admin
from .models import PatientAppointment


# Register your models here.
class AppointAdmin(admin.ModelAdmin):
    list_display = ('hospital',
                    'doctor',
                    'patient',
                    'bloodPressure',
                    'weight',
                    'appointment_date',
                    'appointment_time',
                    'created_at',
                    'updated_at',)


admin.site.register(PatientAppointment, AppointAdmin)
