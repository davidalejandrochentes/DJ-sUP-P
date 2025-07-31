from django import forms
from django.forms import Textarea
from .models import Cliente, Proveedor

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ['user', 'palabras_clave']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre completo'}),
            'teléfono': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': '+53'}),
            'email': forms.EmailInput(attrs={'class': 'form-control m-2', 'placeholder': 'tu_nombre@gmail.com'}),
            'dirección': Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'dirección'}),
            'notas': Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'nota'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        exclude = ['user', 'palabras_clave']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre completo'}),
            'teléfono': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': '+53'}),
            'email': forms.EmailInput(attrs={'class': 'form-control m-2', 'placeholder': 'tu_nombre@gmail.com'}),
            'dirección': Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'dirección'}),
            'notas': Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'nota'}),
        }        