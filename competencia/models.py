from django.db import models
from deporte.models import Arbitro, Atleta

class Evento(models.Model):
    class Estatus(models.TextChoices):
        PROGRAMADO = 'programado', 'Programado'
        EN_CURSO = 'en_curso', 'En curso'
        FINALIZADO = 'finalizado', 'Finalizado'
    nombre = models.CharField(max_length=180)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    sede_lugar = models.CharField(max_length=180)
    estado = models.CharField(max_length=80)
    estatus = models.CharField(max_length=20, choices=Estatus.choices, default=Estatus.PROGRAMADO)
    def __str__(self): return self.nombre

class Categoria(models.Model):
    class Modalidad(models.TextChoices):
        FIGURAS = 'figuras', 'Figuras / Kata'
        COMBATE = 'combate', 'Combate / Kumite'
        DEFENSA = 'defensa', 'Defensa Personal'
    nombre = models.CharField(max_length=140)
    modalidad = models.CharField(max_length=20, choices=Modalidad.choices)
    edad_min = models.PositiveSmallIntegerField(default=0)
    edad_max = models.PositiveSmallIntegerField(default=99)
    sexo = models.CharField(max_length=20, default='Mixto')
    rango_cintas = models.CharField(max_length=100, blank=True)
    def __str__(self): return self.nombre

class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscripciones')
    atleta = models.ForeignKey(Atleta, on_delete=models.PROTECT, related_name='inscripciones')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='inscripciones')
    creada = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['evento', 'atleta', 'categoria'], name='unique_evento_atleta_categoria')]
    def __str__(self): return f'{self.atleta} - {self.categoria}'

class Puntuacion(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='puntuaciones')
    juez = models.ForeignKey(Arbitro, on_delete=models.PROTECT, related_name='puntuaciones')
    ronda = models.PositiveSmallIntegerField(default=1)
    puntos = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    creada = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        self.total = self.puntos
        super().save(*args, **kwargs)
