from django.urls import path
from . import views

urlpatterns = [
    path('categorias_productos/', views.categorias_productos, name="categorias_productos"),
    path('nueva_categoria/', views.nueva_categoria, name="nueva_categoria"),
    path('eliminar_categoria/<int:id>', views.eliminar_categoria, name="eliminar_categoria"),
    path('productos/stock-bajo-general/', views.productos_con_stock_bajo_general, name='productos_stock_bajo_general'),

    path('lista_productos/<int:id>', views.lista_productos, name="lista_productos"),
    path('nuevo_producto/<int:id>', views.nuevo_producto, name="nuevo_producto"),
    path('producto/<int:id>', views.producto, name="producto"),
    path('editar_producto/<int:id>', views.editar_producto, name="editar_producto"),
    path('eliminar_producto/<int:id>', views.eliminar_producto, name="eliminar_producto"),
    path('productos/stock-bajo/<int:id>', views.productos_con_stock_bajo, name='productos_stock_bajo'),
    path('exportar-productos-excel/', views.exportar_productos_excel, name='exportar_productos_excel'),
    path('exportar-productos-categoria-excel/<int:id>/', views.exportar_productos_categoria_excel, name='exportar_productos_categoria_excel'),
    path('exportar-productos-stock-bajo-excel/', views.exportar_productos_stock_bajo_excel, name='exportar_productos_stock_bajo_excel'),
    path('exportar-productos-stock-bajo-categoria-excel/<int:id>/', views.exportar_productos_stock_bajo_categoria_excel, name='exportar_productos_stock_bajo_categoria_excel'),
]