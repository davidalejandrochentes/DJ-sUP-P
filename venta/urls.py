from django.urls import path
from . import views

urlpatterns = [
    path('venta/', views.venta, name="venta"),
    path('nueva/', views.nueva_venta, name='nueva_venta'),
    path('detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('eliminar/<int:venta_id>/', views.eliminar_venta, name='eliminar_venta'),
    path('eliminar-detalle/<int:detalle_id>/', views.eliminar_detalle, name='eliminar_detalle'),
    path('descargar-excel/<int:venta_id>/', views.descargar_venta_excel, name='descargar_venta_excel'),
    path('descargar-ventas-excel/', views.descargar_ventas_excel, name='descargar_ventas_excel'),
]