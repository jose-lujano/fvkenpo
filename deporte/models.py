from django.db import models

class Asociacion(models.Model):
    nombre = models.CharField(max_length=160)
    estado = models.CharField(max_length=80)
    presidente = models.CharField(max_length=140, blank=True)
    telefono = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='asociaciones/', blank=True, null=True)
    def __str__(self): return f'{self.nombre} - {self.estado}'

class Club(models.Model):
    nombre = models.CharField(max_length=160)
    asociacion = models.ForeignKey(Asociacion, on_delete=models.PROTECT, related_name='clubes')
    entrenador_principal = models.CharField(max_length=140, blank=True)
    ciudad_municipio = models.CharField(max_length=100)
    def __str__(self): return self.nombre

class Atleta(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMENINO = 'F', 'Femenino'
        OTRO = 'O', 'Otro'
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=30, unique=True)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    club = models.ForeignKey(Club, on_delete=models.PROTECT, related_name='atletas')
    cinturon_kyu = models.CharField(max_length=80)
    fotografia = models.ImageField(upload_to='atletas/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    def __str__(self): return f'{self.nombres} {self.apellidos}'

class Arbitro(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=30, unique=True)
    nivel_rango = models.CharField(max_length=100)
    estado = models.CharField(max_length=80)
    def __str__(self): return f'{self.nombres} {self.apellidos}'
