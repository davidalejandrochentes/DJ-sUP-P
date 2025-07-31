from django import forms
from django.forms import Textarea
from .models import Categoria, Producto, Proveedor

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre de la categoría'}),
            'descripción': Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'Descripción de la categoría'}),
        }

class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['proveedor'].queryset = Proveedor.objects.filter(user=user)

    class Meta:
        model = Producto
        fields = '__all__'
        exclude = ['user', 'categoría', 'fecha_de_creación']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control m-2', 'placeholder': 'Nombre del producto'}),
            'código': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'código del producto'}),
            'proveedor': forms.Select(attrs={'class': 'form-select m-5', 'placeholder': 'Proveedor del producto'}),
            'descripción': Textarea(attrs={'class': 'form-control m-2', 'placeholder': 'Descripción del producto'}),
            'precio_de_adquisición': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Precio de adquisición'}),
            'precio_de_venta': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Precio de venta'}),
            'unidad_de_medida': forms.Select(attrs={'class': 'form-select m-2', 'placeholder': 'unidad de medida'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'En Stock'}),
            'alerta_stock': forms.NumberInput(attrs={'class': 'form-control m-2', 'type': 'number', 'placeholder': 'Alerta para bajo stock'}),
            }  

    def clean(self):
        cleaned_data = super().clean()
        precio_de_adquisición = cleaned_data.get('precio_de_adquisición')
        precio_de_venta = cleaned_data.get('precio_de_venta')
        stock = cleaned_data.get('stock')
        alerta_stock = cleaned_data.get('alerta_stock')
        código = cleaned_data.get('código')
        
        if precio_de_adquisición:
            if precio_de_adquisición <= 0:
                self.add_error('precio_de_adquisición', 'El precio de adquisición es incorrecto.')
        else:
            self.add_error('precio_de_adquisición', 'El precio de adquisición es incorrecto.')

        if código:
            if precio_de_adquisición <= 0:
                self.add_error('código', 'El código es incorrecto.')
        else:
            self.add_error('código', 'El código es incorrecto.')    

        if precio_de_venta:
            if precio_de_venta <= 0:
                self.add_error('precio_de_venta', 'El precio de venta es incorrecto.')
        else:
            self.add_error('precio_de_venta', 'El precio de venta es incorrecto.')

        if stock:
            if stock <= 0:
                self.add_error('stock', 'El valor de este campo es incorrecto.')
        else:
            self.add_error('stock', 'El valor de este campo es incorrecto.')

        if alerta_stock:
            if alerta_stock <= 0:
                self.add_error('alerta_stock', 'El valor de este campo es incorrecto.')
        else:
            self.add_error('alerta_stock', 'El valor de este campo es incorrecto.')
        
        return cleaned_data 