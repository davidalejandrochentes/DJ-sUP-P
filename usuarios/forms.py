from django import forms
from django.forms import Textarea, CheckboxInput
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
import re

class RegistroUsuarioForm(UserCreationForm):
    DENOMINACION_CHOICES = [
        ("OTRO", "Otro"),
        ("ONG", "ONG"),
        ("CENTRO", "Centro Estatal"),
        ("MIPYME", "MIPYME"),
        ("TCP", "TCP"),
    ]
    COMO_NOS_CONOCIO_CHOICES = [
        ("AMIGO", "Un amigo"),
        ("IG", "Instagram"),
        ("DISCORD", "Discord"),
        ("LINKEDIN", "LinkedIn"),
        ("X", "X (Twitter)"),
        ("FB", "Facebook"),
    ]
    
    telefono = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ej: +53 55123456'
    }))
    direccion = forms.CharField(widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese su dirección completa',
        'rows': 3
    }))
    denominación = forms.ChoiceField(
        choices=DENOMINACION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cómo_nos_conoció = forms.ChoiceField(
        choices=COMO_NOS_CONOCIO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    aprobación_de_privacidad = forms.BooleanField(
        widget=CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 
                 'telefono', 'direccion', 'denominación', 'cómo_nos_conoció', 
                 'aprobación_de_privacidad')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Elija un nombre de usuario único'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repita su contraseña'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Su nombre'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Sus apellidos'
        })

        # Personalizar mensajes de ayuda
        self.fields['password1'].help_text = 'La contraseña debe tener al menos 8 caracteres y no puede ser común.'
        self.fields['username'].help_text = 'Letras, números y @/./+/-/_ solamente.'

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('aprobación_de_privacidad'):
            self.add_error('aprobación_de_privacidad', 'Debe aceptar las políticas de privacidad para crear su cuenta.')
        return cleaned_data

        

class EditarUsuarioForm(forms.ModelForm):
    DENOMINACION_CHOICES = [
        ("OTRO", "Otro"),
        ("ONG", "ONG"),
        ("CENTRO", "Centro Estatal"),
        ("MIPYME", "MIPYME"),
        ("TCP", "TCP"),
    ]
    COMO_NOS_CONOCIO_CHOICES = [
        ("AMIGO", "Un amigo"),
        ("IG", "Instagram"),
        ("DISCORD", "Discord"),
        ("LINKEDIN", "LinkedIn"),
        ("X", "X (Twitter)"),
        ("FB", "Facebook"),
    ]
    
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Elija un nombre de usuario único'
        })
    )
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Su nombre'
        })
    )
    last_name = forms.CharField(
        label="Apellidos",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sus apellidos'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )
    telefono = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono',
            'min': '1000000',
            'max': '9999999999999',
            'pattern': '\d*',
            'title': 'Solo se permiten números'
        })
    )
    direccion = forms.CharField(
        required=False,
        widget=Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su dirección completa',
            'rows': 3
        })
    )
    denominación = forms.ChoiceField(
        required=False,
        choices=DENOMINACION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'aria-label': 'Seleccione su denominación'
        })
    )
    cómo_nos_conoció = forms.ChoiceField(
        required=False,
        choices=COMO_NOS_CONOCIO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'aria-label': 'Seleccione cómo nos conoció'
        })
    )

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono', 'direccion', 
                 'denominación', 'cómo_nos_conoció')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Validar que el nombre de usuario sea único
        if Usuario.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elija otro.")
        return username
    
    def clean_teléfono(self):
        teléfono = self.cleaned_data.get('teléfono')
        if teléfono is not None:
            if len(str(abs(telefono))) < 7:
                raise forms.ValidationError('El número de teléfono debe tener al menos 7 dígitos.')
            if len(str(abs(telefono))) > 13:
                raise forms.ValidationError('El número de teléfono no puede tener más de 13 dígitos.')
        return teléfono
    
    def save(self, commit=True):
        # Convert username to lowercase before saving
        user = super().save(commit=False)
        user.username = user.username.lower()
        if commit:
            user.save()
        return user 



class ReactivationForm(forms.Form):
    usuario = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    nombre = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    apellido = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )
    teléfono = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono',
            'min': '1000000',
            'max': '9999999999999',
            'pattern': '\d*',
            'title': 'Solo se permiten números'
        })
    )

    nro_transaccion = forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de transferencia',
            'pattern': '[A-Z0-9]{1,13}',
            'title': 'Solo letras mayúsculas y números, máximo 13 caracteres',
            'oninput': 'this.value = this.value.toUpperCase()'
        })
    )

    def clean_nro_transaccion(self):
        nro_transaccion = self.cleaned_data.get('nro_transaccion', '').strip().upper()
        if not nro_transaccion:
            raise forms.ValidationError('El número de transferencia no puede estar vacío.')
        if len(nro_transaccion) > 13:
            raise forms.ValidationError('El número de transferencia no puede exceder 13 caracteres.')
        if not re.match(r'^[A-Z0-9]+$', nro_transaccion):
            raise forms.ValidationError('El número de transacción solo puede contener letras mayúsculas y números.')
        return nro_transaccion