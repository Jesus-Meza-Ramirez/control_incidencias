# control_incidencias/urls.py
from django.contrib import admin
from django.urls import path, include     # <-- include agregado
from django.conf import settings
from webui.views import exportar_incidencias_excel
from django.conf.urls.static import static
from webui.views import (
    login_view, logout_view, dashboard_redirect,
    panel_control_interno, panel_admin_terminal, panel_admin_sistema, actualizar_estado_control_interno
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth y home
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', dashboard_redirect, name='home'),

    # Paneles principales
    path('panel/control-interno/', panel_control_interno, name='panel_control_interno'),
    path('panel/admin-terminal/', panel_admin_terminal, name='panel_admin_terminal'),
    path('panel/admin-sistema/', panel_admin_sistema, name='panel_admin_sistema'),

    # Apps con include
    path("incidencias/", include("incidencias.urls")),
    path("webui/", include("webui.urls")),  # 👈 FALTABA ESTO


    path('panel/reportes/export-excel/', exportar_incidencias_excel, name='export_excel'),
    
    
    path("ci/estado/", actualizar_estado_control_interno, name="actualizar_estado_control_interno"),

    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
