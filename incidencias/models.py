from django.db import models

class Terminal(models.Model):
    id_terminal = models.CharField(max_length=10, primary_key=True, db_column='id_terminal')
    nombre_terminal = models.CharField(max_length=50, db_column='nombre_terminal')

    def __str__(self):
        return self.nombre_terminal

    class Meta:
        db_table = 'terminales'   # ← nombre real de tu tabla
        managed = False           # ← NO tocar el esquema


class BoleteroCajero(models.Model):
    id_bc = models.AutoField(primary_key=True, db_column='id_bc')
    nombre = models.CharField(max_length=50, db_column='nombre')
    usuario = models.CharField(max_length=20, db_column='usuario', null=True, blank=True)
    cargo = models.CharField(max_length=10, choices=[('boletero','Boletero'),('cajero','Cajero')], db_column='cargo')
    estado = models.CharField(max_length=10, choices=[('activo','Activo'),('inactivo','Inactivo')], db_column='estado')
    # importante: indicar la columna FK real
    id_terminal = models.ForeignKey(
        Terminal,
        on_delete=models.PROTECT,          # o CASCADE si así está en tu BD
        db_column='id_terminal',
        related_name='boleteros'           # útil para consultas
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'boleteros_cajeros'     # ← ojo al nombre exacto de tu tabla
        managed = False


class Incidencia(models.Model):
    ESTADOS = [
        ('conforme', 'Conforme'),
        ('observado', 'Observado'),
        ('pendiente', 'Pendiente'),
        ('resuelto', 'Resuelto'),
    ]
    id_incidencia = models.AutoField(primary_key=True, db_column='id_incidencia')
    id_bc = models.ForeignKey(
        BoleteroCajero,
        on_delete=models.CASCADE,
        db_column='id_bc',
        related_name='incidencias'
    )
    id_usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='incidencias'
    )
    fecha_incidencia = models.DateField(db_column='fecha_incidencia')
    
    tipo_incidencia = models.CharField(
    max_length=50,
    db_column='tipo_incidencia',
    blank=True,
    
    )

    motivo = models.TextField(blank=True, null=True)
    
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='observado',      #
        db_column='estado'
    )
    evidencia = models.ImageField(upload_to='evidencias/', blank=True, null=True, db_column='evidencia')
    fecha_revision = models.DateField(db_column='fecha_revision', null=True, blank=True)
    
    
    
    solucion_admin = models.TextField(
        blank=True,
        null=True,
        db_column='solucion_admin'
    )

    evidencia_solucion = models.ImageField(
        upload_to='evidencias_solucion/',
        blank=True,
        null=True,
        db_column='evidencia_solucion'
    )

    fecha_solucion = models.DateField(
        null=True,
        blank=True,
        db_column='fecha_solucion'
    )
    
    
    
    def __str__(self):
        return f"{self.tipo_incidencia} - {self.id_bc.nombre}"

    class Meta:
        db_table = 'incidencias'
        managed = False
        
    
