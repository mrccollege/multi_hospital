from django.urls import path
from . import views

urlpatterns = [
    path('patient-appointment/', views.patient_appointment, name='patient_appointment'),
    path('patient_appointment_list/', views.patient_appointment_list, name='patient_appointment_list'),
    path('patient-search/', views.patient_search, name='patient_search'),
    path('doctor-search/', views.doctor_search, name='doctor_search'),
    path('get_ward_price/', views.get_ward_price, name='get_ward_price'),
]
