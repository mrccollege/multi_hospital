from django.urls import path
from .import views
urlpatterns = [
    path('history/<int:appoint_id>/', views.patient_history_report, name='patient_history_report'),
    path('get_history/', views.get_history, name='get_history'),
]
