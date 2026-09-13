from django.contrib import admin
from .models import Categoria, Evento, Inscripcion, Puntuacion

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'sede_lugar', 'estatus')
    list_filter = ('estatus', 'estado')
    search_fields = ('nombre', 'sede_lugar')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'modalidad', 'edad_min', 'edad_max', 'sexo')
    list_filter = ('modalidad', 'sexo')

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('evento', 'atleta', 'categoria')
    list_filter = ('evento', 'categoria')
    search_fields = ('atleta__nombres', 'atleta__apellidos')

@admin.register(Puntuacion)
class PuntuacionAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'juez', 'ronda', 'puntos', 'total')
    list_filter = ('ronda', 'juez')
