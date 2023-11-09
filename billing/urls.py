from django.urls import path
from .import views
urlpatterns = [
    path('logout/', views.mini_store_logout, name='mini_store_logout'),
    path('patient_billing_list/', views.patient_billing_list, name='patient_billing_list'),
    path('generate_bill/<int:head_id>/', views.generate_bill, name='generate_bill'),
    path('generated_bill/<int:id>/', views.generated_bill, name='generated_bill'),

]
