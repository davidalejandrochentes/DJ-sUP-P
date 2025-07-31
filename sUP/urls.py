from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('agenda/', include('agenda.urls')),
    path('stock/', include('stock.urls')),
    path('venta/', include('venta.urls')),
    path('reporte/', include('reporte.urls')),
    path('ia/', include('ia.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
