from django.contrib import admin
from .models import CustomUser, HospitalUser, DoctorUser, Stores, PatientUser, SocialMediaReference, OtherReference


class SocialReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_reference', 'created_at')


class OtherReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('h_id', 'user')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('d_id', 'user', 'hospital')


class StoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store_type', 'hospital')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('p_id', 'user', 'hospital')


admin.site.register(CustomUser)
admin.site.register(HospitalUser, HospitalAdmin)
admin.site.register(DoctorUser, DoctorAdmin)
admin.site.register(Stores, StoresAdmin)
admin.site.register(PatientUser, PatientAdmin)
admin.site.register(SocialMediaReference, SocialReferenceAdmin)
admin.site.register(OtherReference, OtherReferenceAdmin)
