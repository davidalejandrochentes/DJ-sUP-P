from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class CustomUserAdmin(UserAdmin):
    # Define los campos que se mostrarán en las vistas de administración de usuarios
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'telefono', 'direccion', 'denominación', 'cómo_nos_conoció', 'último_pago', 'nro_transacción')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Para los formularios de creación de usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'telefono', 'direccion', 'denominación', 'cómo_nos_conoció', 'último_pago', 'nro_transacción'),
        }),
    )
    
    # Define las columnas que se mostrarán en la lista de usuarios en el panel de admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'telefono', 'último_pago', 'nro_transacción')
    
    # Agregar filtro de estado activo y número de transacción
    list_filter = ('is_active', 'nro_transacción')

admin.site.register(Usuario, CustomUserAdmin)