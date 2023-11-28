from django.contrib import admin

from .models import LookupField


# Register your models here.
class LookupFieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'title', 'hospital']


admin.site.register(LookupField, LookupFieldAdmin)
