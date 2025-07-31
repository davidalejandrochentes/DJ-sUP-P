from django.db import models
from django.conf import settings
from agenda.models import Proveedor

# Create your models here.
class Categoria(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, null=False, blank=False)
    descripción = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),  # Índice para mejorar consultas por usuario
            models.Index(fields=['nombre']),  # Índice para búsquedas por nombre
        ]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    TIPO_STOCK_CHOICES = [
        ("UNIDADES", "Unidades"),
        ("KILOGRAMOS", "Kilogramos"),
        ("LITROS", "Litros"),
        ("PALETS", "Palets"),
        ("METROS CÚBICOS", "Metros cúbicos"),
        ("PROYECTOS", "Proyectos"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoría = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=40, null=False, blank=False)
    código = models.IntegerField(null=False, blank=False)
    descripción = models.CharField(max_length=255, blank=True, null=True)
    precio_de_adquisición = models.DecimalField(max_digits=10, verbose_name="Coste de adquisición", decimal_places=2, null=False, blank=False)
    precio_de_venta = models.DecimalField(max_digits=10, verbose_name="Precio de venta", decimal_places=2, null=False, blank=False)
    unidad_de_medida = models.CharField(max_length=20, default="Unidades", choices=TIPO_STOCK_CHOICES, verbose_name="Este producto se vende por")
    stock = models.IntegerField(null=False, blank=False)
    alerta_stock = models.PositiveIntegerField(default=10, verbose_name="Alerta de inventario", help_text="Nivel de stock que activa la alerta")
    fecha_de_creación = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", null=False, blank=False)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['categoría']),
            models.Index(fields=['nombre']),
            models.Index(fields=['stock']),
            models.Index(fields=['alerta_stock']),
            models.Index(fields=['código']),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.código})"