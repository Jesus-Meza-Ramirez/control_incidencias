
from django.contrib import admin
from .models import Incidencia, BoleteroCajero, Terminal

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_incidencia',
        'get_boletero_nombre',
        'get_boletero_usuario',
        'get_terminal',  
        'get_control_interno',
        'estado',
        'motivo',
        'get_fecha_revision',
        'evidencia',
          
    )

    # ——— columnas calculadas ———
    def get_boletero_nombre(self, obj):
        return obj.id_bc.nombre if obj.id_bc else '—'
    get_boletero_nombre.short_description = 'Nombre Boletero/Cajero'

    def get_boletero_usuario(self, obj):
        return obj.id_bc.usuario if obj.id_bc else '—'
    get_boletero_usuario.short_description = 'Usuario'
    
    def get_terminal(self, obj):
        term = getattr(obj.id_bc, 'id_terminal',None)
        return str(term) if term else '—'
    get_terminal.short_description = 'terminal'
    get_terminal.admin_order_field = 'id_bc__id_terminal'

    def get_control_interno(self, obj):
        return obj.id_usuario.nombre if obj.id_usuario else '—'
    get_control_interno.short_description = 'Usuario Control Interno'

    def get_fecha_revision(self, obj):
        # Si tu modelo TIENE el campo fecha_revision, lo mostramos
        if hasattr(obj, 'fecha_revision'):
            return obj.fecha_revision or '—'
        # Si tu modelo NO tiene ese campo, no hay nada que mostrar
        return '—'
    get_fecha_revision.short_description = 'Fecha de Revisión'
    
    
    
    list_filter = ('estado', 'tipo_incidencia', 'fecha_incidencia','fecha_revision')
    search_fields = (
        'id_bc__nombre',
        'id_bc__usuario',            
        'id_usuario__nombre',
        'motivo',
    )
    ordering = ('-fecha_incidencia',)
    

@admin.register(BoleteroCajero)
class BoleteroCajeroAdmin(admin.ModelAdmin):
    list_display = ('id_bc', 'nombre', 'usuario', 'cargo', 'estado', 'id_terminal')
    list_filter = ('estado', 'cargo','id_terminal')
    search_fields = ('nombre', 'usuario')
    ordering = ('nombre',)
    
@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('id_terminal', 'nombre_terminal')
    #list_filter = ('estado', 'cargo')
    #search_fields = ('nombre', 'usuario')
    #ordering = ('nombre',)

