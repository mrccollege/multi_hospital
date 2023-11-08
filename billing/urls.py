from django.urls import path
from .import views
urlpatterns = [
    path('login/', views.mini_store_login, name='mini_store_login'),
    path('logout/', views.mini_store_logout, name='mini_store_logout'),
    path('', views.patient_billing_list, name='patient_billing_list'),
    path('generate_bill/<int:id>/', views.generate_bill, name='generate_bill'),
    path('bill_generated/<int:id>/', views.bill_generated, name='bill_generated'),

]
