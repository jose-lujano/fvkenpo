from django.urls import path
from .views import boletin_resultados, eventos, reportes, reporte_categoria, reporte_categoria_pdf
urlpatterns = [
    path('', eventos, name='eventos'),
    path('reportes/', reportes, name='reportes'),
    path('resultados/', boletin_resultados, name='boletin_resultados'),
    path('categorias/<int:categoria_id>/reporte/', reporte_categoria, name='reporte_categoria'),
    path('categorias/<int:categoria_id>/reporte/pdf/', reporte_categoria_pdf, name='reporte_categoria_pdf'),
]