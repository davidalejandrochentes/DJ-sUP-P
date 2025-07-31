from django import forms
from django.forms import Textarea
from .models import Venta, DetalleVenta, Cliente

class VentaForm(forms.ModelForm):
    TIPO_CLIENTE_CHOICES = [
        ('registrado', 'Cliente Registrado'),
        ('minorista', 'Cliente Desconocido')
    ]
    tipo_cliente = forms.ChoiceField(
        choices=TIPO_CLIENTE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input m-2'}),
        initial='minorista',
        required=True
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cliente'].queryset = Cliente.objects.filter(user=user)
        
        # Si es una instancia existente, establecer el tipo_cliente basado en si tiene cliente o no
        if self.instance and self.instance.pk:
            self.initial['tipo_cliente'] = 'registrado' if self.instance.cliente else 'minorista'
            # Para debug
            print("Instance cliente:", self.instance.cliente)
            print("Initial tipo_cliente:", self.initial['tipo_cliente'])

    def clean(self):
        cleaned_data = super().clean()
        tipo_cliente = cleaned_data.get('tipo_cliente')
        cliente = cleaned_data.get('cliente')
        
        # Para debug
        print("Clean - tipo_cliente:", tipo_cliente)
        print("Clean - cliente:", cliente)

        # Si es cliente minorista, asegurarse de que no haya cliente seleccionado
        if tipo_cliente == 'minorista':
            cleaned_data['cliente'] = None
        # Si es cliente registrado, asegurarse de que haya un cliente seleccionado
        elif tipo_cliente == 'registrado' and not cliente:
            self.add_error('cliente', 'Debe seleccionar un cliente para una venta registrada')
            raise forms.ValidationError('Debe seleccionar un cliente cuando el tipo es "Cliente Registrado"')

        return cleaned_data

    def save(self, commit=True):
        venta = super().save(commit=False)
        # Para debug
        print("Save - cliente antes:", venta.cliente)
        print("Save - cleaned_data:", self.cleaned_data)
        
        # Asegurarse de que el cliente se guarde correctamente
        if self.cleaned_data.get('tipo_cliente') == 'minorista':
            venta.cliente = None
        else:
            venta.cliente = self.cleaned_data.get('cliente')
        
        print("Save - cliente después:", venta.cliente)
        
        if commit:
            venta.save()
        return venta

    class Meta:
        model = Venta
        fields = ('tipo_cliente', 'cliente', 'código')
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select m-2', 'placeholder': 'Cliente'}),
            'código': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Código de venta'}),
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ('producto', 'cantidad')
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-select m-2',
                'placeholder': 'Buscar producto por nombre o código'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control m-2',
                'type': 'number',
                'placeholder': 'Cantidad'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        producto = cleaned_data.get('producto')

        if cantidad and producto:
            if cantidad <= 0:
                self.add_error('cantidad', 'La cantidad debe ser mayor que 0.')
            elif cantidad > producto.stock:
                self.add_error('cantidad', f'No hay suficiente stock para {producto.nombre}. Stock actual: {producto.stock}')

        return cleaned_data