from datetime import timedelta
from django.utils import timezone

def pago_context(request):
    fecha_limite = None
    mostrar_alerta = False  # Controlará si se muestra el div

    if request.user.is_authenticated and request.user.último_pago:
        # Calcula la fecha límite
        fecha_limite = request.user.último_pago + timedelta(days=30)
        
        # Verifica si faltan 5 días o menos para la fecha límite
        if fecha_limite - timedelta(days=5) <= timezone.now() <= fecha_limite:
            mostrar_alerta = True

    return {'fecha_limite': fecha_limite, 'mostrar_alerta': mostrar_alerta}
