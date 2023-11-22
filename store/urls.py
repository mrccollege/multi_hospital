from django.urls import path
from . import views

urlpatterns = [
    path('main_medical_store_dashboard/', views.main_medical_store_dashboard, name='main_medical_store_dashboard'),
    path('mini_medical_store_dashboard/', views.mini_medical_store_dashboard, name='mini_medical_store_dashboard'),
    path('add_medicine/<int:main_store_id>/', views.add_medicine, name='add_medicine'),
    path('search-medicine/', views.search_medicine, name='search_medicine'),
    path('transfer-search-medicine/', views.transfer_search_medicine, name='transfer_search_medicine'),

    path('view_mini_stores_record/<int:mini_store_id>/<int:hospital_id>/', views.view_mini_stores_record, name='view_mini_stores_record'),

    path('get_mini_store_model_data/', views.get_mini_store_model_data, name='get_mini_store_model_data'),
    path('transfer_medicine/', views.transfer_medicine, name='transfer_medicine'),
    path('new_transfer_medicine/', views.new_transfer_medicine, name='new_transfer_medicine'),
    path('transfer_medicine_from_mini/', views.transfer_medicine_from_mini, name='transfer_medicine_from_mini'),
    path('transfer_medicine_mini_to_mini_store/', views.transfer_medicine_mini_to_mini_store, name='transfer_medicine_mini_to_mini_store'),
]
