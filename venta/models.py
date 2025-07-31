from django.db import models
from django.conf import settings
from agenda.models import Cliente
from stock.models import Producto
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Venta(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(verbose_name="Fecha de la venta")
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente asociado")
    código = models.IntegerField(default=0, null=False, blank=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total de la venta", default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),  # Índice para mejorar consultas por usuario
            models.Index(fields=['código']),  # Índice para búsquedas por nombre
            models.Index(fields=['cliente']),
            models.Index(fields=['fecha']),
        ]

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

    def delete(self, *args, **kwargs):
        for detalle in self.detalles.all():
            # Devolver el stock del producto solo si existe
            if detalle.producto:
                detalle.producto.stock += detalle.cantidad
                detalle.producto.save()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Calcular el total solo si la venta ya existe
        if self.pk:
            self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        super().save(*args, **kwargs)      
    

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_producto = models.CharField(max_length=40, verbose_name="Nombre del producto", null=True)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad vendida", default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario", default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal", default=0)

    def __str__(self):
        if self.producto:
            return f"{self.producto.nombre} - {self.cantidad} unidades"
        return f"{self.nombre_producto} - {self.cantidad} unidades"

    def save(self, *args, **kwargs):
        # Actualizar el stock del producto y calcular subtotal
        if self.pk:
            detalle_anterior = DetalleVenta.objects.get(pk=self.pk)
            diferencia_cantidad = self.cantidad - detalle_anterior.cantidad
            if self.producto:
                if diferencia_cantidad > 0:
                    self.producto.stock -= diferencia_cantidad
                elif diferencia_cantidad < 0:
                    self.producto.stock -= diferencia_cantidad
        else:
            if self.producto:
                self.producto.stock -= self.cantidad
                # Guardar el nombre del producto al momento de la venta
                self.nombre_producto = self.producto.nombre

        if self.producto:
            self.precio_unitario = self.producto.precio_de_venta
            self.subtotal = self.cantidad * self.precio_unitario

        if self.producto:
            self.producto.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Devolver el stock al eliminar el detalle
        if self.producto:
            self.producto.stock += self.cantidad
            self.producto.save()
    
        # Actualizar el total de la venta
        venta = self.venta
        super().delete(*args, **kwargs)  # Primero elimina el detalle
        venta.total = sum(detalle.subtotal for detalle in venta.detalles.all())
        venta.save()  # Guarda la venta con el nuevo total

#------------------------------------------------------------------------------------

@receiver(post_save, sender=DetalleVenta)
def actualizar_total_venta(sender, instance, **kwargs):
    venta = instance.venta
    venta.total = sum(detalle.subtotal for detalle in venta.detalles.all())
    venta.save()