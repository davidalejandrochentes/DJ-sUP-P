from django.db import models
from django.conf import settings

# Modelo Cliente
class Cliente(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=True, null=True)
    teléfono = models.CharField(max_length=15, blank=False, null=False)
    dirección = models.CharField(max_length=255, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    palabras_clave = models.ManyToManyField('PalabraClave', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=True, null=True)
    teléfono = models.CharField(max_length=15, blank=False, null=False)
    dirección = models.CharField(max_length=255, blank=True, null=True)    
    notas = models.TextField(blank=True, null=True)
    palabras_clave = models.ManyToManyField('PalabraClave', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return self.nombre


class PalabraClave(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    palabra = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['palabra']),
        ]
        unique_together = ['user', 'palabra']

    def __str__(self):
        return self.palabra
