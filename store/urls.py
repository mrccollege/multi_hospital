from django.urls import path
from . import views

urlpatterns = [
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('search-medicine/', views.search_medicine, name='search_medicine'),
    path('transfer-search-medicine/', views.transfer_search_medicine, name='transfer_search_medicine'),
    path('mapping-medicine/', views.mapping_medicine, name='mapping_medicine'),
    path('view_main_store/<int:main_store_id>/', views.view_main_store, name='view_main_store'),

    path('get_mini_store_model_data/', views.get_mini_store_model_data, name='get_mini_store_model_data'),
    path('transfer_medicine_to_mini_store/', views.transfer_medicine_to_mini_store, name='transfer_medicine_to_mini_store'),
]
