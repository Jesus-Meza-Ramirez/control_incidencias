# webui/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from usuarios.models import Usuario
from incidencias.models import Incidencia  # <- tu modelo de incidencias (ajusta import si cambia)
from django.db.models import Q, Count, Case, When, IntegerField

from datetime import date
from django.core.paginator import Paginator, EmptyPage


from django.utils import timezone
from django.urls import reverse

from incidencias.models import BoleteroCajero, Terminal



    
def _require_session(request):
    """Redirect to login si no hay sesión."""
    if not request.session.get('uid'):
        return redirect('login')
    return None

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.session.get('uid'):
        return redirect('home')

    if request.method == "POST":
        usuario = (request.POST.get('usuario') or '').strip()   # <- usa el name del input
        contrasena = (request.POST.get('contrasena') or '').strip()

        user = Usuario.objects.filter(
            usuario_login__iexact=usuario,
            contrasena=contrasena
        ).first()

        if not user:
            messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            request.session['uid']      = user.id_usuario
            request.session['nombre']   = user.nombre
            request.session['rol']      = user.rol
            request.session['terminal'] = user.id_terminal_id  # puede ser None
            return redirect('home')

    return render(request, 'login_full.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def dashboard_redirect(request):
    # Si no hay sesión → login
    if not request.session.get('uid'):
        return redirect('login')

    rol = (request.session.get('rol') or '').lower()

    # 👉 ahora sí, si es control interno lo mandamos a TU panel
    if rol == 'control_interno':
        return redirect('panel_control_interno')

    # Ajusta estos destinos cuando implementes los otros paneles:
    if rol in ('admin_terminal', 'terminal'):
        return redirect('panel_admin_terminal')   # de momento lo mandamos a un placeholder
    if rol in ('admin_sistema', 'admin'):
        return redirect('panel_admin_sistema')    # placeholder

    # por defecto
    return redirect('panel_control_interno')



# ============================
#  PANEL CONTROL INTERNO (UI)
# ============================
def panel_control_interno(request):
    maybe_redirect = _require_session(request)
    if maybe_redirect:
        return maybe_redirect

    # ---- Parámetros GET para filtro de fechas (DateField) ----
    rev_desde = request.GET.get('rev_desde')  # 'YYYY-MM-DD'
    rev_hasta = request.GET.get('rev_hasta')  # 'YYYY-MM-DD'

    # ---- Query base (más recientes primero por fecha_revision) ----
    qs = (
        Incidencia.objects
        .select_related('id_bc', 'id_usuario')
        .order_by('-fecha_revision', '-id_incidencia')
    )

    # ---- Filtro por rango de fechas si se envían ambos ----
    if rev_desde and rev_hasta:
        try:
            d1 = date.fromisoformat(rev_desde)
            d2 = date.fromisoformat(rev_hasta)
            if d1 > d2:
                d1, d2 = d2, d1
            # fecha_revision es DateField => usar __range directamente
            qs = qs.filter(fecha_revision__range=(d1, d2))
            qs = qs.filter(fecha_revision__isnull=False)
        except ValueError:
            # Si hay formato inválido, ignoramos el filtro
            pass

    # ---- Cap de 5 páginas máx (20 por página => 100 registros) ----
    qs = qs[:100]

    # ---- Paginación (20 por página) ----
    per_page = 20
    paginator = Paginator(qs, per_page)
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        page_num = 1

    try:
        page_obj = paginator.page(page_num)
    except EmptyPage:
        page_obj = paginator.page(1)

    # ---- Construcción de filas para la tabla ----
    rows = []
    for inc in page_obj.object_list:
        # Fecha incidencia
        fecha = getattr(inc, 'fecha_incidencia', None)

        # Boletero/Cajero
        bc = getattr(inc, 'id_bc', None)
        bc_nombre = getattr(bc, 'nombre', '—')
        bc_usuario = getattr(bc, 'usuario', '—')
        bc_cargo   = getattr(bc, 'cargo', '—') if bc else '—'

        # Terminal (nombre si hay FK; si no, el código)
        term_obj = getattr(bc, 'id_terminal', None)
        terminal = getattr(term_obj, 'nombre', None) if term_obj else None
        if not terminal:
            terminal = getattr(bc, 'id_terminal', '—')

        # Control interno (usuario que registró la incidencia)
        ci_obj = getattr(inc, 'id_usuario', None)
        control_interno = getattr(ci_obj, 'nombre', '—')

        # Estado y demás campos
        estado_val = getattr(inc, 'estado', '') or ''
        estado = 'Observación' if estado_val.lower() == 'observado' else 'Conforme'
        motivo = getattr(inc, 'motivo', '—')

        #evidencia_val = getattr(inc, 'evidencia', '')
        #evidencia = evidencia_val.url if hasattr(evidencia_val, 'url') else (evidencia_val or '')
        
        evidencia_val = getattr(inc, 'evidencia', None)
        evidencia = evidencia_val.url if evidencia_val else ''

        fecha_revision = getattr(inc, 'fecha_revision', None)

        rows.append({
            'fecha': fecha,
            'nombre': bc_nombre,
            'usuario': bc_usuario,
            'cargo': bc_cargo,
            'terminal': terminal,
            'control_interno': control_interno,
            'estado': estado,
            'motivo': motivo,
            'evidencia': evidencia,
            'fecha_revision': fecha_revision,
        })

    # Para preservar el filtro en los links de paginación
    preserved = ''
    if rev_desde:
        preserved += f'&rev_desde={rev_desde}'
    if rev_hasta:
        preserved += f'&rev_hasta={rev_hasta}'

    context = {
        'usuario_nombre': request.session.get('nombre', 'Usuario'),
        'terminal_actual': request.session.get('terminal') or '—',
        'rows': rows,

        # Paginación
        'page_obj': page_obj,
        'preserved': preserved,
        'rev_desde': rev_desde or '',
        'rev_hasta': rev_hasta or '',
        # Aquí agregamos los boleteros
        'boleteros': BoleteroCajero.objects.all(),
        "terminales": Terminal.objects.all().order_by("id_terminal")
        
    }
    return render(request, 'control_interno_dashboard.html', context)


# ============================
#  PLACEHOLDERS (puedes cambiar luego)
# ============================
#def panel_admin_terminal(request):
 #   maybe_redirect = _require_session(request)
 #   if maybe_redirect: 
 #       return maybe_redirect
 #   return render(request, 'placeholder.html', {'titulo': 'Panel Admin Terminal'})

def panel_admin_terminal(request):
    # 1. Verificar sesión
    maybe_redirect = _require_session(request)
    if maybe_redirect:
        return maybe_redirect

    # 2. Obtener usuario logueado y su terminal
    uid = request.session.get('uid')
    user = (
        Usuario.objects
        .select_related('id_terminal')
        .filter(pk=uid)
        .first()
    )

    terminal_id = None
    terminal_name = '—'

    if user and user.id_terminal_id:
        terminal_id = user.id_terminal_id                 # ID numérico del terminal
        terminal_name = getattr(user.id_terminal, 'nombre_terminal', str(user.id_terminal_id))

    # 3. Filtros de fecha (usamos fecha_revision igual que en control interno)
    rev_desde = request.GET.get('rev_desde')  # 'YYYY-MM-DD'
    rev_hasta = request.GET.get('rev_hasta')  # 'YYYY-MM-DD'

    # 4. Query base: incidencias SOLO del terminal del usuario
    qs = (
        Incidencia.objects
        .select_related('id_bc', 'id_usuario', 'id_bc__id_terminal')
        .order_by('-fecha_revision', '-id_incidencia')
    )

    if terminal_id is not None:
        qs = qs.filter(id_bc__id_terminal_id=terminal_id)

    # 5. Filtro por rango de fechas (fecha_revision)
    if rev_desde and rev_hasta:
        try:
            d1 = date.fromisoformat(rev_desde)
            d2 = date.fromisoformat(rev_hasta)
            if d1 > d2:
                d1, d2 = d2, d1

            qs = qs.filter(fecha_revision__range=(d1, d2))
            qs = qs.filter(fecha_revision__isnull=False)
        except ValueError:
            # Formato raro → ignoramos filtro
            pass

    # Guardamos este queryset para las tarjetas
    qs_for_cards = qs

    # 6. Paginación (20 por página)
    per_page = 20
    paginator = Paginator(qs, per_page)
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        page_num = 1

    try:
        page_obj = paginator.page(page_num)
    except EmptyPage:
        page_obj = paginator.page(1)

    # 7. Construcción de filas para la tabla
    rows = []
    for inc in page_obj.object_list:
        # Fecha de incidencia
        fecha = getattr(inc, 'fecha_incidencia', None)

        # Boletero/Cajero
        bc = getattr(inc, 'id_bc', None)
        bc_nombre = getattr(bc, 'nombre', '—')
        bc_usuario = getattr(bc, 'usuario', '—')
        bc_cargo   = getattr(bc, 'cargo', '—') if bc else '—'

        # Terminal (nombre si hay FK; si no, el código)
        term_obj = getattr(bc, 'id_terminal', None)
        terminal_txt = getattr(term_obj, 'nombre', None) if term_obj else None
        if not terminal_txt:
            terminal_txt = getattr(bc, 'id_terminal', '—')

        # Control interno
        ci_obj = getattr(inc, 'id_usuario', None)
        control_interno = getattr(ci_obj, 'nombre', '—')

        # Estado
        estado_val = getattr(inc, 'estado', '') or ''
        estado = 'Observación' if estado_val.lower() == 'observado' else 'Conforme'
        motivo = getattr(inc, 'motivo', '—')

        # Evidencia
        #evidencia_val = getattr(inc, 'evidencia', '')
        #evidencia = evidencia_val.url if hasattr(evidencia_val, 'url') else (evidencia_val or '')
        evidencia_val = getattr(inc, 'evidencia', None)
        evidencia = evidencia_val.url if evidencia_val else ''

        fecha_revision = getattr(inc, 'fecha_revision', None)

        rows.append({
            'fecha': fecha,
            'nombre': bc_nombre,
            'usuario': bc_usuario,
            'cargo': bc_cargo,
            'terminal': terminal_txt,
            'control_interno': control_interno,
            'estado': estado,
            'motivo': motivo,
            'evidencia': evidencia,
            'fecha_revision': fecha_revision,
        })

    # 8. Tarjetas de resumen (usamos el mismo queryset filtrado por terminal)
    cards = {
        'activas': qs_for_cards.count(),
        'pendientes': qs_for_cards.filter(estado__iexact='observado').count(),
        'resueltas': qs_for_cards.filter(estado__iexact='conforme').count(),
    }

    # 9. Preservar filtros de fecha en los links de paginación
    preserved = ''
    if rev_desde:
        preserved += f'&rev_desde={rev_desde}'
    if rev_hasta:
        preserved += f'&rev_hasta={rev_hasta}'

    # 10. Contexto para el template
    context = {
        'usuario_nombre': request.session.get('nombre', 'Usuario'),
        'terminal_name': terminal_name,    # ← este es el que usa tu HTML
        'rows': rows,
        'cards': cards,

        'page_obj': page_obj,
        'preserved': preserved,
        'rev_desde': rev_desde or '',
        'rev_hasta': rev_hasta or '',
    }
    return render(request, 'admin_terminal_dashboard.html', context)


def panel_admin_sistema(request):
    # 1) Requiere sesión
    if not request.session.get('uid'):
        return redirect('login')

    # 2) Query base de usuarios (con la FK a terminal si existe)
    qs = (
        Usuario.objects
        .select_related('id_terminal')   # asumiendo que tu FK se llama así
        .order_by('id_usuario')          # cambia si prefieres otra orden
    )

    # 3) (Opcional) Búsqueda rápida ?q=
    q = (request.GET.get('q') or '').strip()
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) |
            Q(usuario_login__icontains=q) |
            Q(rol__icontains=q) |
            Q(id_terminal__nombre__icontains=q) |
            Q(id_terminal__icontains=q)  # por si ID/código viene como texto
        )

    # 4) Paginación
    paginator = Paginator(qs, 12)
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        page_num = 1
    try:
        page_obj = paginator.page(page_num)
    except EmptyPage:
        page_obj = paginator.page(1)

    # 5) Adaptar filas al template (tolerante a campos ausentes)
    usuarios_rows = []
    for u in page_obj.object_list:
        # fecha ingreso (usa el que tengas)
        fecha_ing = getattr(u, 'fecha_ingreso', None) or getattr(u, 'fecha_creacion', None)

        # terminal: si es FK con nombre, úsalo; si no, muestra el valor tal cual
        term_obj = getattr(u, 'id_terminal', None)
        term_name = getattr(term_obj, 'nombre', None) if term_obj else None
        if not term_name:
            term_name = term_obj or '—'

        # activo: booleano o string
        activo_val = getattr(u, 'activo', None)
        if activo_val is None:
            # intenta con estado/flag alternativos
            estado = (getattr(u, 'estado', '') or '').lower()
            activo_bool = estado in ('activo', 'activa', '1', 'true', 'sí', 'si')
        else:
            activo_bool = bool(activo_val)

        usuarios_rows.append({
            'fecha_ingreso': fecha_ing,
            'nombre': getattr(u, 'nombre', '—'),
            'usuario_login': getattr(u, 'usuario_login', '—'),
            'rol': getattr(u, 'rol', '—'),
            'terminal': term_name,
            'activo': activo_bool,
        })

    # 6) Contexto para el template
    context = {
        'usuario_nombre': request.session.get('nombre', 'Usuario'),
        'usuarios': usuarios_rows,
        'page_obj': page_obj,
    }
    return render(request, 'admin_sistema_dashboard.html', context)


#def panel_admin_sistema(request):
 #   maybe_redirect = _require_session(request)
 #   if maybe_redirect: 
 #       return maybe_redirect
 #   return render(request, 'placeholder.html', {'titulo': 'Panel Admin Sistema'})











