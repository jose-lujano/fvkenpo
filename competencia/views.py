from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.db.models import Sum
from .models import Categoria, Evento, Inscripcion, Puntuacion

def eventos(request):
    return render(request, 'competencia/eventos.html', {'eventos': Evento.objects.order_by('-fecha_inicio')})

def reporte_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    inscripciones = Inscripcion.objects.filter(categoria=categoria).select_related('atleta', 'atleta__club', 'evento')
    return render(request, 'competencia/reporte_categoria.html', {'categoria': categoria, 'inscripciones': inscripciones})

def reporte_categoria_pdf(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    template = get_template('competencia/reporte_categoria_pdf.html')
    html = template.render({'categoria': categoria, 'inscripciones': Inscripcion.objects.filter(categoria=categoria).select_related('atleta', 'atleta__club')})
    try:
        from xhtml2pdf import pisa
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="reporte-{categoria_id}.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response
    except ImportError:
        return HttpResponse('Instala xhtml2pdf para generar el PDF.', status=503)

def boletin_resultados(request):
    resultados = Puntuacion.objects.values(
        'inscripcion__atleta__nombres', 'inscripcion__atleta__apellidos',
        'inscripcion__atleta__club__nombre', 'inscripcion__atleta__club__asociacion__nombre',
    ).annotate(total=Sum('total')).order_by('-total')
    return render(request, 'competencia/boletin_resultados.html', {'resultados': resultados})
