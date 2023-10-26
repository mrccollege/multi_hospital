from django.urls import path
from . import views

urlpatterns = [
    path('hospital_registration/', views.hospital_registration, name='hospital_registration'),
    path('doctor_registration/', views.doctor_registration, name='doctor_registration'),
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('main_medical_store_registration/', views.main_medical_store_registration, name='main_medical_store_registration'),
    path('mini_medical_store_registration/', views.mini_medical_store_registration, name='mini_medical_store_registration'),
]
