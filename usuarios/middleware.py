from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.safestring import mark_safe

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Ignorar rutas administrativas, autenticación y pago
            rutas_ignoradas = ['/admin/', '/login/', '/pagar/']
            if not any(request.path.startswith(ruta) for ruta in rutas_ignoradas):
                if request.user.último_pago:
                    if timezone.now() > request.user.último_pago + timezone.timedelta(days=30):
                        # Desactivar la cuenta
                        request.user.is_active = False
                        request.user.save()
                        mensaje = 'Tu suscripción ha vencido. <a href="/pagar/" class="alert-link">Haz clic aquí para realizar el pago</a>'
                        messages.error(request, mark_safe(mensaje))
                        return redirect('log_in')

        response = self.get_response(request)
        return response