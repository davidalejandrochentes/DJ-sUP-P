from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('login/', views.log_in, name="log_in"),
    path('log_out/', views.log_out, name="log_out"),
    path('politicas/', views.politicas, name="politicas"),
    path('mis_datos/', views.mis_datos, name="mis_datos"),
    path('editar_datos/', views.editar_datos, name="editar_datos"),
    path('cambiar_password/', views.cambiar_password, name="cambiar_password"),
    path('pagar/', views.pagar, name="pagar"),
    path('agradecer/', views.agradecer, name="agradecer"),
    path('registro/', views.registro, name='registro'),
    path('reactivar/', views.reactivar, name="reactivar"),
]