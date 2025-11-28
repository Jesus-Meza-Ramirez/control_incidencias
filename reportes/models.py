from django.db import models

class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True, db_column='id_reporte')
    id_usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    fecha_generacion = models.DateTimeField(auto_now_add=True, db_column='fecha_generacion')
    tipo_reporte = models.CharField(max_length=50, db_column='tipo_reporte')
    archivo_reporte = models.CharField(max_length=255, null=True, blank=True, db_column='archivo_reporte')

    def __str__(self):
        return f"{self.tipo_reporte} - {self.fecha_generacion.strftime('%d/%m/%Y')}"

    class Meta:
        db_table = 'reportes'   # nombre real de tu tabla en MySQL
        managed = False         
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

