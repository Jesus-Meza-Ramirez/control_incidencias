from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nombre = models.CharField(max_length=50, db_column='nombre')
    usuario_login = models.CharField(max_length=30, unique=True, db_column='usuario_login')
    contrasena = models.CharField(max_length=128, db_column='contrasena')  # almacenarás hash aquí
    rol = models.CharField(max_length=20, db_column='rol')
    id_terminal = models.ForeignKey('incidencias.Terminal',models.SET_NULL, null=True, blank=True, db_column='id_terminal')

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

    class Meta:
        db_table = 'usuarios'  # fijar el nombre de tabla
        managed = False


