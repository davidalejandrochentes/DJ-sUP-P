from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .forms import RegistroUsuarioForm, EditarUsuarioForm, ReactivationForm
from .models import Usuario
from django.contrib.auth.forms import PasswordChangeForm

from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import logging
from django.views.decorators.cache import never_cache


logger = logging.getLogger(__name__)

def enviar_mensaje_telegram(mensaje):
    """Envía un mensaje de Telegram de forma asíncrona con manejo de errores."""
    async def send_message():
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            await bot.send_message(
                chat_id=settings.TELEGRAM_CHAT_ID, 
                text=mensaje
            )
        except TelegramError as e:
            logger.error(f"Error enviando mensaje de Telegram: {e}")
    
    try:
        asyncio.run(send_message())
    except Exception as e:
        logger.error(f"Error en envío de mensaje de Telegram: {e}")

@never_cache
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_active = True  # El usuario estará activo desde el inicio
            usuario.save()
            login(request, usuario)
            return redirect('agradecer')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
@never_cache
def log_out(request):
    logout(request)
    return redirect('inicio')

@never_cache
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        try:
            user = Usuario.objects.get(username=username)
            if not user.is_active:
                mensaje = 'Tu cuenta ha sido desactivada. <a href="/reactivar/" class="alert-link">Haz clic aquí para realizar el pago</a>'
                messages.error(request, mark_safe(mensaje))
            else:
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('inicio')
                else:
                    messages.error(request, "El usuario no existe o la contraseña es incorrecta.")
        except Usuario.DoesNotExist:
            messages.error(request, "El usuario no existe o la contraseña es incorrecta.")
    
    return render(request, 'usuarios/login.html', {})

@login_required
@never_cache
def pagar(request):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/pagar.html', {'modo': 'no_autenticado'})
    
    if not request.user.is_active:
        return render(request, 'usuarios/pagar.html', {
            'modo': 'renovacion',
            'usuario': request.user
        })
    
    if request.method == 'POST':
        nro_transaccion = request.POST.get('nro_transaccion', '').strip().upper()
    
        if not nro_transaccion:
            return redirect('pagar')
        
        if len(nro_transaccion) > 13:
            return redirect('pagar')
        
        if not all(caracter.isalnum() for caracter in nro_transaccion):
            return redirect('pagar')
        
        request.user.nro_transacción = nro_transaccion
        request.user.save()
        return redirect('pagar')
    
    return render(request, 'usuarios/pagar.html', {'modo': 'normal'})


def inicio(request):
    return render(request, 'usuarios/inicio.html', {})


def politicas(request):
    return render(request, 'usuarios/politicas.html', {})   


def agradecer(request):
    return render(request, 'usuarios/agradecer.html', {})        


@login_required
@never_cache
def mis_datos(request):
    return render(request, 'usuarios/mis_datos.html', {})    


@login_required
@never_cache
def editar_datos(request):
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mis_datos')
    else:
        form = EditarUsuarioForm(instance=request.user)
    
    return render(request, 'usuarios/editar_datos.html', {
        'form': form
    })


@login_required
@never_cache
def cambiar_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Mantener la sesión activa
            messages.success(request, 'Tu contraseña ha sido actualizada exitosamente.')
            return redirect('mis_datos')
    else:
        password_form = PasswordChangeForm(request.user)
    
    # Aplicar clases de Bootstrap a los campos de contraseña
    password_form.fields['old_password'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Ingrese su contraseña actual'
    })
    password_form.fields['new_password1'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Ingrese su nueva contraseña'
    })
    password_form.fields['new_password2'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Confirme su nueva contraseña'
    })
    
    return render(request, 'usuarios/cambiar_password.html', {
        'password_form': password_form
    })

@never_cache
def reactivar(request):
    if request.method == 'POST':
        form = ReactivationForm(request.POST)
        if form.is_valid():
            # Process the reactivation form
            usuario = form.cleaned_data['usuario']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            teléfono = form.cleaned_data['teléfono']
            nro_transaccion = form.cleaned_data['nro_transaccion']

            mensaje = f"✅​ *Reactivacion de cuenta* 💸​\n\n" \
                f"Usuario: {usuario}\n" \
                f"Nombre: {nombre}\n" \
                f"Apellidos: {apellido}\n" \
                f"Teléfono: {teléfono}\n" \
                f"Nro transacción: {nro_transaccion}\n" \
            
            enviar_mensaje_telegram(mensaje)
            
            return render(request, 'usuarios/reactivar.html', {
                'form': form, 
                'success_message': 'Solicitud de reactivación enviada. Un administrador la revisará antes de cumplidas 3 horas.'
            })
    else:
        form = ReactivationForm()
    
    return render(request, 'usuarios/reactivar.html', {'form': form})

