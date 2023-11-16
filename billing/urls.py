from django.urls import path
from .import views
urlpatterns = [
    path('logout/', views.mini_store_logout, name='mini_store_logout'),
    path('patient_billing_list/', views.patient_billing_list, name='patient_billing_list'),
    path('generate_bill/<int:head_id>/', views.generate_bill, name='generate_bill'),
    path('generated_bill/<int:id>/', views.generated_bill, name='generated_bill'),
    path('send_email/<int:bill_id>/', views.send_email, name='send_email'),
    path('generated_billing_list/', views.generated_billing_list, name='generated_billing_list'),
    path('new_customer_bill/', views.new_customer_bill, name='new_customer_bill'),
    path('new_customer_generate_bill/<int:bill_id>/', views.new_customer_generate_bill, name='new_customer_generate_bill'),

]
