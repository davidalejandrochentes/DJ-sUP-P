from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    denominación = models.CharField(max_length=10, blank=True, null=True)
    cómo_nos_conoció = models.CharField(max_length=10, blank=True, null=True)
    último_pago = models.DateTimeField(default=timezone.now)
    nro_transacción = models.CharField(max_length=13, blank=True, null=True)


    def __str__(self):
        return self.username