from django.db import models

class Usuario(models.Model):

    ROLES = [
        ('admin_terminal', 'Administrador de Terminal'),
        ('admin_sistema', 'Administrador del Sistema'),
        ('control_interno', 'Control Interno'),
    ]

    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nombre = models.CharField(max_length=50, db_column='nombre')
    usuario_login = models.CharField(max_length=30, unique=True, db_column='usuario_login')
    contrasena = models.CharField(max_length=128, db_column='contrasena')

    fecha_ingreso = models.DateField(db_column='fecha_ingreso')

    rol = models.CharField(
        max_length=20,
        db_column='rol',
        choices=ROLES,
        default='admin_terminal'
    )

    id_terminal = models.ForeignKey(
        'incidencias.Terminal',
        models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_terminal'
    )

    # ➕ NUEVO CAMPO
    activo = models.BooleanField(default=True, db_column='activo')

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

    class Meta:
        db_table = 'usuarios'
        managed = False
