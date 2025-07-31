from django.urls import path
from . import views

urlpatterns = [
    path('reporte', views.reporte, name="reporte"),
    path('productos_mas_vendidos/', views.productos_mas_vendidos, name="productos_mas_vendidos"),
    path('ganancias_por_cliente/', views.ganancias_por_cliente, name="ganancias_por_cliente"),
    path('ingresos_por_producto/', views.ingresos_por_producto, name="ingresos_por_producto"),
    path('productos_con_mayor_interes/', views.productos_con_mayor_interes, name="productos_con_mayor_interes"),
    path('exportar-productos-margen-excel/', views.exportar_productos_margen_excel, name='exportar_productos_margen_excel'),
    path('exportar-ganancias-cliente-excel/', views.exportar_ganancias_cliente_excel, name='exportar_ganancias_cliente_excel'),
    path('exportar-productos-vendidos-excel/', views.exportar_productos_vendidos_excel, name='exportar_productos_vendidos_excel'),
    path('exportar-ingresos-producto-excel/', views.exportar_ingresos_producto_excel, name='exportar_ingresos_producto_excel'),
]