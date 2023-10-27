from django.contrib import admin
from .models import HeaderPatient, DetailsPatient

# Register your models here.

admin.site.register(HeaderPatient)
admin.site.register(DetailsPatient)
