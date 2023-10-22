from django.urls import path
from . import views

urlpatterns = [
    path('patient-appointment/', views.patient_appointment, name='patient_appointment'),
    path('patient-search/', views.patient_search, name='patient_search'),
    path('doctor-search/', views.doctor_search, name='doctor_search'),
]
