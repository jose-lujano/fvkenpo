from django.core.validators import RegexValidator
from django.db import models

hex_color = RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Use un color HEX válido, por ejemplo #003366.')

class SiteSetting(models.Model):
    sitio_nombre = models.CharField(max_length=180, default='TORNEOS NACIONALES ABIERTOS DE ARTES MARCIALES')
    logo = models.ImageField(upload_to='config/', blank=True, null=True)
    fondo_pantalla = models.ImageField(upload_to='config/', blank=True, null=True)
    color_primario_start = models.CharField(max_length=7, default='#003366', validators=[hex_color])
    color_primario_end = models.CharField(max_length=7, default='#0066cc', validators=[hex_color])
    email_contacto = models.EmailField(blank=True)
    telefono_contacto = models.CharField(max_length=40, blank=True)
    direccion = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sitio_nombre

class EmailSetting(models.Model):
    smtp_host = models.CharField(max_length=180, default='smtp.gmail.com')
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_user = models.EmailField(blank=True)
    smtp_password = models.CharField(max_length=255, blank=True)
    smtp_use_tls = models.BooleanField(default=True)
    from_email = models.EmailField(blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Configuración de correo SMTP'

class Album(models.Model):
    titulo = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    class Meta:
        ordering = ['-fecha']
    def __str__(self):
        return self.titulo

class GaleriaImagen(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='galeria/')
    titulo = models.CharField(max_length=160, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    creada = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titulo or f'Imagen de {self.album}'

class ContactMessage(models.Model):
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=40, default='')
    email = models.EmailField()
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    ciudad = models.CharField(max_length=100, default='')
    asunto = models.CharField(max_length=180, default='Contacto web')
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)
    class Meta:
        ordering = ['-creado']
