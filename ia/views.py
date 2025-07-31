from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from venta.models import Venta, DetalleVenta
from stock.models import Producto
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from django.db.models.functions import ExtractWeekDay
from django.db.models import Avg, Count, Sum, F, FloatField, OuterRef, Subquery
from django.db.models.functions import ExtractHour, Cast, Coalesce
from django.db.models.functions import ExtractWeekDay, Cast, Coalesce, ExtractMonth
from django.views.decorators.cache import cache_page


@login_required
@cache_page(300)
def consejos(request):
    # Obtener el usuario actual
    user = request.user
    
    consejos = []
    
    # 1. Análisis de productos con stock bajo
    productos_stock_bajo = Producto.objects.filter(
        user=user,
        stock__lte=F('alerta_stock')
    )
    if productos_stock_bajo.exists():
        consejos.append({
            'tipo': 'alerta',
            'mensaje': f'Tienes {productos_stock_bajo.count()} productos con stock bajo. '
                      'Considera hacer un pedido pronto para evitar quedarte sin inventario.'
        })
    
    # 2. Análisis de ventas recientes (últimos 30 días)
    fecha_inicio = timezone.now() - timedelta(days=30)
    ventas_recientes = Venta.objects.filter(
        user=user,
        fecha__gte=fecha_inicio
    )
    
    total_ventas = 0  # Inicializar total_ventas con un valor por defecto
    if ventas_recientes.exists():
        total_ventas = ventas_recientes.aggregate(total=Sum('total'))['total']
        promedio_diario = total_ventas / 30 if total_ventas else 0
        
        consejos.append({
            'tipo': 'ventas',
            'mensaje': f'En los últimos 30 días has vendido un total de ${total_ventas:.2f}, '
                      f'con un promedio diario de ${promedio_diario:.2f}.'
        })
        
        # 3. Productos más vendidos
        productos_top = DetalleVenta.objects.filter(
            venta__user=user,
            venta__fecha__gte=fecha_inicio
        ).values('producto__nombre').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido')[:3]
        
        if productos_top:
            mensaje_productos = "Tus productos más vendidos son: "
            mensaje_productos += ", ".join([f"{p['producto__nombre']} ({p['total_vendido']} unidades)" 
                                         for p in productos_top])
            consejos.append({
                'tipo': 'productos_top',
                'mensaje': mensaje_productos
            })
    
    # 4. Productos sin movimiento
    productos_sin_movimiento = Producto.objects.filter(
        user=user
    ).exclude(
        id__in=DetalleVenta.objects.filter(
            venta__user=user,
            venta__fecha__gte=fecha_inicio
        ).values('producto_id')
    )
    
    if productos_sin_movimiento.exists():
        consejos.append({
            'tipo': 'sin_movimiento',
            'mensaje': f'Tienes {productos_sin_movimiento.count()} productos sin ventas en los últimos 30 días. '
                      'Considera hacer una promoción especial para estos productos.'
        })

        # 5. Análisis de rentabilidad por producto
    productos_rentabilidad = Producto.objects.filter(user=user).annotate(
        margen=(F('precio_de_venta') - F('precio_de_adquisición')) / F('precio_de_adquisición') * 100
    ).order_by('margen')

    productos_baja_rentabilidad = productos_rentabilidad.filter(margen__lt=20)
    if productos_baja_rentabilidad.exists():
        consejos.append({
            'tipo': 'rentabilidad',
            'mensaje': f'Tienes {productos_baja_rentabilidad.count()} productos con margen de ganancia menor al 20%. '
                      'Considera revisar sus precios de venta o buscar proveedores más económicos.'
        })

    # 6. Análisis de tendencias de ventas
    ventas_mes_anterior = Venta.objects.filter(
        user=user,
        fecha__gte=fecha_inicio - timedelta(days=30),
        fecha__lt=fecha_inicio
    ).aggregate(total=Sum('total'))['total'] or 0

    if ventas_mes_anterior > 0:
        variacion = ((total_ventas - ventas_mes_anterior) / ventas_mes_anterior) * 100
        mensaje_tendencia = (
            f'Tus ventas han {"aumentado" if variacion > 0 else "disminuido"} un {abs(variacion):.1f}% '
            f'respecto al mes anterior. '
        )
        if variacion < 0:
            mensaje_tendencia += 'Considera implementar estrategias de marketing o promociones especiales.'
        consejos.append({
            'tipo': 'tendencia',
            'mensaje': mensaje_tendencia
        })

    # 7. Análisis de clientes frecuentes
    clientes_frecuentes = Venta.objects.filter(
        user=user,
        fecha__gte=fecha_inicio,
        cliente__isnull=False
    ).values('cliente__nombre').annotate(
        total_compras=Count('id'),
        valor_total=Sum('total')
    ).order_by('-total_compras')[:5]

    if clientes_frecuentes:
        mensaje_clientes = "Tus mejores clientes del mes son: "
        for cliente in clientes_frecuentes:
            mensaje_clientes += f"\n- {cliente['cliente__nombre']}: {cliente['total_compras']} compras por ${cliente['valor_total']:.2f}"
        consejos.append({
            'tipo': 'clientes',
            'mensaje': mensaje_clientes
        })

    # 8. Consejos de gestión de inventario
    productos_exceso = Producto.objects.filter(
        user=user,
        stock__gt=F('alerta_stock') * 3
    )
    if productos_exceso.exists():
        consejos.append({
            'tipo': 'inventario',
            'mensaje': f'Tienes {productos_exceso.count()} productos con stock muy alto. '
                      'Considera hacer promociones especiales para reducir el inventario y liberar capital.'
        })

    # 9. Análisis de ventas por día de la semana
    ventas_por_dia = Venta.objects.filter(
        user=user,
        fecha__gte=fecha_inicio
    ).annotate(
        dia_semana=ExtractWeekDay('fecha')
    ).values('dia_semana').annotate(
        total_ventas=Sum('total')
    ).order_by('-total_ventas')

    if ventas_por_dia:
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        mejor_dia = dias[ventas_por_dia[0]['dia_semana']-1]
        consejos.append({
            'tipo': 'dias',
            'mensaje': f'Tu mejor día de ventas es {mejor_dia}. '
                      'Considera aumentar el personal o el inventario durante este día.'
        })

    # 10. Consejos de precios
    productos_sin_margen = Producto.objects.filter(
        user=user,
        precio_de_venta__lte=F('precio_de_adquisición') * 1.1
    )
    if productos_sin_margen.exists():
        consejos.append({
            'tipo': 'precios',
            'mensaje': f'Tienes {productos_sin_margen.count()} productos con margen menor al 10%. '
                      'Revisa tu estrategia de precios para asegurar la rentabilidad.'
        }) 

    # 11. Análisis de categorías más rentables
    categorias_rentables = DetalleVenta.objects.filter(
        venta__user=user,
        venta__fecha__gte=fecha_inicio
    ).values('producto__categoría__nombre').annotate(
        total_ventas=Sum('subtotal'),
        cantidad_vendida=Sum('cantidad')
    ).order_by('-total_ventas')[:3]

    if categorias_rentables:
        mensaje_categorias = "Tus categorías más rentables son: "
        mensaje_categorias += ", ".join([f"{c['producto__categoría__nombre']} (${c['total_ventas']:.2f})" 
                                     for c in categorias_rentables])
        consejos.append({
            'tipo': 'categorias',
            'mensaje': mensaje_categorias + ". Considera expandir estas líneas de productos."
        })

    # 12. Análisis de velocidad de rotación de inventario
    productos_rotacion = Producto.objects.filter(
        user=user
    ).annotate(
        ventas_mes=Coalesce(Subquery(
            DetalleVenta.objects.filter(
                producto=OuterRef('pk'),
                venta__fecha__gte=fecha_inicio
            ).values('producto').annotate(
                total_vendido=Sum('cantidad')
            ).values('total_vendido')[:1]
        ), 0)
    ).annotate(
        rotacion=F('ventas_mes') / Cast('stock', FloatField()) * 100
    )

    productos_baja_rotacion = productos_rotacion.filter(rotacion__lt=10, stock__gt=0)
    if productos_baja_rotacion.exists():
        consejos.append({
            'tipo': 'rotacion',
            'mensaje': f'Tienes {productos_baja_rotacion.count()} productos con baja rotación (menos del 10% mensual). '
                      'Considera estrategias para aumentar su visibilidad o reducir su stock.'
        })

    # 13. Análisis de horarios pico de ventas
    if ventas_recientes.exists():
        ventas_por_hora = Venta.objects.filter(
            user=user,
            fecha__gte=fecha_inicio
        ).annotate(
            hora=ExtractHour('fecha')
        ).values('hora').annotate(
            total_ventas=Count('id')
        ).order_by('-total_ventas')

        if ventas_por_hora:
            hora_pico = ventas_por_hora[0]['hora']
            consejos.append({
                'tipo': 'horario',
                'mensaje': f'Tu hora pico de ventas es a las {hora_pico}:00. '
                          'Asegúrate de tener suficiente personal y stock durante estas horas.'
            })

    # 14. Análisis de proveedores y costos
    proveedores_productos = Producto.objects.filter(
        user=user
    ).values('proveedor__nombre').annotate(
        total_productos=Count('id'),
        costo_promedio=Avg('precio_de_adquisición')
    ).order_by('-total_productos')

    if proveedores_productos:
        proveedor_principal = proveedores_productos[0]
        consejos.append({
            'tipo': 'proveedores',
            'mensaje': f'Tu principal proveedor es {proveedor_principal["proveedor__nombre"]} '
                      f'con {proveedor_principal["total_productos"]} productos. '
                      'Considera negociar mejores precios por volumen.'
        })

    # 15. Análisis de tendencias de categorías
    tendencias_categorias = DetalleVenta.objects.filter(
        venta__user=user,
        venta__fecha__gte=fecha_inicio
    ).values('producto__categoría__nombre').annotate(
        ventas_recientes=Sum('cantidad')
    ).order_by('-ventas_recientes')

    ventas_mes_anterior_cat = DetalleVenta.objects.filter(
        venta__user=user,
        venta__fecha__gte=fecha_inicio - timedelta(days=30),
        venta__fecha__lt=fecha_inicio
    ).values('producto__categoría__nombre').annotate(
        ventas_anteriores=Sum('cantidad')
    )

    if tendencias_categorias and ventas_mes_anterior_cat:
        categoria_creciente = None
        mayor_crecimiento = 0
        
        for cat_actual in tendencias_categorias:
            cat_anterior = next(
                (x for x in ventas_mes_anterior_cat 
                 if x['producto__categoría__nombre'] == cat_actual['producto__categoría__nombre']),
                None
            )
            if cat_anterior and cat_anterior['ventas_anteriores'] > 0:
                crecimiento = ((cat_actual['ventas_recientes'] - cat_anterior['ventas_anteriores']) 
                             / cat_anterior['ventas_anteriores'] * 100)
                if crecimiento > mayor_crecimiento:
                    mayor_crecimiento = crecimiento
                    categoria_creciente = cat_actual['producto__categoría__nombre']

        if categoria_creciente:
            consejos.append({
                'tipo': 'tendencia_categoria',
                'mensaje': f'La categoría {categoria_creciente} muestra el mayor crecimiento '
                          f'({mayor_crecimiento:.1f}%). Considera invertir más en esta categoría.'
            })

    # 16. Análisis de fidelización de clientes
    total_clientes = Venta.objects.filter(
        user=user,
        fecha__gte=fecha_inicio,
        cliente__isnull=False
    ).values('cliente').distinct().count()

    clientes_recurrentes = Venta.objects.filter(
        user=user,
        fecha__gte=fecha_inicio,
        cliente__isnull=False
    ).values('cliente').annotate(
        compras=Count('id')
    ).filter(compras__gt=1).count()

    if total_clientes > 0:
        tasa_recurrencia = (clientes_recurrentes / total_clientes) * 100
        consejos.append({
            'tipo': 'fidelizacion',
            'mensaje': f'Tu tasa de clientes recurrentes es del {tasa_recurrencia:.1f}%. '
                      f'{"¡Excelente trabajo!" if tasa_recurrencia > 50 else "Considera implementar un programa de fidelización."}'
        })

    # 17. Análisis de ventas por temporada
    ventas_por_mes = Venta.objects.filter(
        user=user,
        fecha__gte=fecha_inicio - timedelta(days=365)  # Último año
    ).annotate(
        mes=ExtractMonth('fecha')
    ).values('mes').annotate(
        total_ventas=Sum('total')
    ).order_by('-total_ventas')

    if ventas_por_mes:
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        mejor_mes = meses[ventas_por_mes[0]['mes']-1]
        consejos.append({
            'tipo': 'temporada',
            'mensaje': f'Tu mejor mes de ventas es {mejor_mes}. '
                      'Prepárate con anticipación para aprovechar esta temporada alta.'
        })

    # 18. Análisis de eficiencia de precios
    productos_margen_alto = productos_rentabilidad.filter(
        margen__gt=50,
        stock__gt=0
    ).order_by('-margen')[:5]

    if productos_margen_alto:
        mensaje_margen = "Productos con mejor margen: "
        mensaje_margen += ", ".join([f"{p.nombre} ({p.margen:.1f}%)" for p in productos_margen_alto])
        consejos.append({
            'tipo': 'margen_alto',
            'mensaje': mensaje_margen + ". Considera promocionar más estos productos."
        })

    # 19. Análisis de diversificación de proveedores
    dependencia_proveedor = Producto.objects.filter(
        user=user
    ).values('proveedor').annotate(
        total_productos=Count('id')
    ).order_by('-total_productos')
    total_productos = Producto.objects.filter(user=user).count()
    if dependencia_proveedor and dependencia_proveedor[0]['total_productos'] > total_productos * 0.5:
        consejos.append({
            'tipo': 'diversificacion',
            'mensaje': 'Más del 50% de tus productos dependen de un solo proveedor. '
                  'Considera diversificar tus fuentes de suministro para reducir riesgos.'
    })

    # 20. Análisis de valor promedio de venta
    if ventas_recientes.exists():
        valor_promedio_venta = total_ventas / ventas_recientes.count()
        consejos.append({
            'tipo': 'ticket_promedio',
            'mensaje': f'Tu ticket promedio de venta es ${valor_promedio_venta:.2f}. '
                      f'{"Considera estrategias de venta cruzada para aumentar este valor." if valor_promedio_venta < 100 else "¡Buen trabajo con las ventas de alto valor!"}'
        })         

    return render(request, 'ia/consejos_ia.html', {
        'consejos': consejos
    })