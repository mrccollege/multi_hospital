from django.contrib import admin
from .models import CustomUser, HospitalUser, DoctorUser, PatientUser


# Register your models here.
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('h_id', 'user')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('d_id', 'user')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('p_id', 'user')


admin.site.register(CustomUser)
admin.site.register(HospitalUser, HospitalAdmin)
admin.site.register(DoctorUser, DoctorAdmin)
admin.site.register(PatientUser, PatientAdmin)
