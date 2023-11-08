from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('appointment/', include('appointment.urls')),
    path('doctor/', include('doctor.urls')),
    path('', include('dashboard.urls')),
    path('store/', include('store.urls')),
    path('patient_report/', include('patient_report.urls')),
    path('billing/', include('billing.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
