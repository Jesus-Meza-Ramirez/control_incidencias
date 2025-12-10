from django.contrib import admin
from django.utils import timezone
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'id_usuario',
        'nombre',
        'usuario_login',
        'rol',
        'id_terminal',
        'activo',
        'fecha_ingreso',
    )

    list_filter = ('rol', 'activo')
    search_fields = ('nombre', 'usuario_login')

    # Usamos un campo “falso” solo para mostrar
    readonly_fields = ('fecha_ingreso_display',)

    # Orden de campos en el formulario
    fields = (
        'nombre',
        'usuario_login',
        'contrasena',
        'rol',
        'id_terminal',
        'activo',
        'fecha_ingreso_display',   # <- aparece como "Fecha de ingreso"
    )

    def fecha_ingreso_display(self, obj):
        """
        Lo que se muestra en el admin:
        - Si el usuario ya existe: muestra su fecha_ingreso real.
        - Si es un usuario nuevo: muestra la fecha de hoy.
        """
        if obj and obj.pk and obj.fecha_ingreso:
            return obj.fecha_ingreso
        return timezone.localdate()

    fecha_ingreso_display.short_description = "Fecha de ingreso"

    def save_model(self, request, obj, form, change):
        """
        Cuando se crea un usuario nuevo, si no tiene fecha_ingreso,
        se le pone la fecha de hoy.
        """
        if not change and not obj.fecha_ingreso:
            obj.fecha_ingreso = timezone.localdate()
        super().save_model(request, obj, form, change)


