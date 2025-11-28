#from django.contrib import admin
#from .models import Usuario

#admin.site.register(Usuario)

from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre', 'usuario_login', 'rol', 'id_terminal')

