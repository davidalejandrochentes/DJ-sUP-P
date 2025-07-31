from django.urls import path
from . import views

urlpatterns = [
    path('proveedores/', views.proveedores, name="proveedores"),
    path('proveedor/<int:id>', views.proveedor, name="proveedor"),
    path('eliminar_proveedor/<int:id>', views.eliminar_proveedor, name="eliminar_proveedor"),
    path('nuevo_proveedor', views.nuevo_proveedor, name="nuevo_proveedor"),
    path('editar_proveedor/<int:id>', views.editar_proveedor, name="editar_proveedor"),
    path('proveedor/<int:proveedor_id>/agregar-palabra-clave/', views.agregar_palabra_clave_proveedor, name='agregar_palabra_clave_proveedor'),
    path('proveedor/<int:proveedor_id>/eliminar-palabra-clave/<int:palabra_id>/', views.eliminar_palabra_clave_proveedor, name='eliminar_palabra_clave_proveedor'),
    
    path('clientes/', views.clientes, name="clientes"),
    path('cliente/<int:id>', views.cliente, name="cliente"),
    path('eliminar_cliente/<int:id>', views.eliminar_cliente, name="eliminar_cliente"),
    path('nuevo_cliente', views.nuevo_cliente, name="nuevo_cliente"),
    path('editar_cliente/<int:id>', views.editar_cliente, name="editar_cliente"),
    path('cliente/<int:cliente_id>/agregar-palabra-clave/', views.agregar_palabra_clave, name='agregar_palabra_clave'),
    path('cliente/<int:cliente_id>/eliminar-palabra-clave/<int:palabra_id>/', views.eliminar_palabra_clave, name='eliminar_palabra_clave'),
    path('exportar-clientes-excel/', views.exportar_clientes_excel, name='exportar_clientes_excel'),
    path('exportar-proveedores-excel/', views.exportar_proveedores_excel, name='exportar_proveedores_excel'),
]