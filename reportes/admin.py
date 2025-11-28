#from django.contrib import admin
#from .models import Reporte

#admin.site.register(Reporte)

from django.contrib import admin
from .models import Reporte

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id_reporte','tipo_reporte','fecha_generacion','id_usuario')
