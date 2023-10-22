from django.contrib import admin
from .models import MiniMedicalStore, MainMedicalStore, MiniStoreMedicine, Medicine

# Register your models here.
admin.site.register(MainMedicalStore)
admin.site.register(MiniMedicalStore)
admin.site.register(Medicine)
admin.site.register(MiniStoreMedicine)
