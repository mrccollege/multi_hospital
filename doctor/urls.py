from django.urls import path
from .import views
urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('login/', views.doctor_login, name='doctor_login'),
    path('logout/', views.doctor_logout, name='doctor_logout'),
]
