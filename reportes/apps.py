from django.apps import AppConfig


class ReportesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reportes'
    #label = 'app_reportes'  # ✅ label único para evitar duplicado
    verbose_name = 'Reportes'
