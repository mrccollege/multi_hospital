from django.contrib import admin
from .models import CustomUser, HospitalUser, DoctorUser, PatientUser


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('h_id', 'user')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('d_id', 'user', 'hospital')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('p_id', 'user', 'hospital')


admin.site.register(CustomUser)
admin.site.register(HospitalUser, HospitalAdmin)
admin.site.register(DoctorUser, DoctorAdmin)
admin.site.register(PatientUser, PatientAdmin)
