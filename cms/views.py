from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
import logging
from smtplib import SMTPAuthenticationError
from competencia.models import Evento
from .forms import ContactForm
from .models import Album, ContactMessage, EmailSetting, GaleriaImagen, SiteSetting

logger = logging.getLogger(__name__)

def _process_contact_form(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        contact_message = form.save(commit=False)
        contact_message.asunto = 'Contacto web'
        contact_message.save()
        setting = SiteSetting.objects.first()
        email_setting = EmailSetting.objects.first()
        recipient = setting.email_contacto if setting else ''
        if recipient and not (email_setting and email_setting.smtp_host and email_setting.smtp_user and email_setting.smtp_password):
            logger.error('SMTP no configurado en el módulo de configuración de correo.')
            messages.warning(request, 'El mensaje fue guardado, pero el correo del sitio no tiene SMTP configurado.')
        elif recipient:
            try:
                connection = get_connection(
                    backend=settings.EMAIL_BACKEND,
                    host=email_setting.smtp_host,
                    port=email_setting.smtp_port,
                    username=email_setting.smtp_user,
                    password=email_setting.smtp_password,
                    use_tls=email_setting.smtp_use_tls,
                )
                email = EmailMessage(
                    subject=f'[FVK] {contact_message.asunto}',
                    body=(
                        f'Nombre: {contact_message.nombre}\n'
                        f'Teléfono: {contact_message.telefono}\n'
                        f'Correo: {contact_message.email}\n'
                        f'Edad: {contact_message.edad or "No indicada"}\n'
                        f'Ciudad: {contact_message.ciudad}\n\n'
                        f'{contact_message.mensaje}'
                    ),
                    to=[recipient],
                    reply_to=[contact_message.email],
                    from_email=email_setting.from_email or email_setting.smtp_user,
                    connection=connection,
                )
                sent = email.send(fail_silently=False)
                if sent != 1:
                    raise RuntimeError('El servidor SMTP no aceptó el mensaje.')
                logger.info('Mensaje de contacto %s aceptado por SMTP. Message-ID: %s', contact_message.pk, email.message()['Message-ID'])
                messages.success(request, 'Tu mensaje ha sido enviado satisfactoriamente')
            except SMTPAuthenticationError:
                logger.exception('Gmail rechazó las credenciales SMTP del mensaje %s.', contact_message.pk)
                messages.warning(request, 'El mensaje fue guardado, pero Gmail rechazó las credenciales SMTP. Usa una contraseña de aplicación.')
            except Exception:
                logger.exception('No se pudo enviar el mensaje de contacto %s.', contact_message.pk)
                messages.warning(request, 'El mensaje fue guardado, pero no pudo enviarse por correo. Revisa la configuración SMTP.')
        else:
            messages.success(request, 'Tu mensaje fue guardado. El administrador aún no ha configurado su correo.')
        return None
    return form

def home(request):
    albums = Album.objects.filter(activo=True).annotate(total_imagenes=Count('imagenes'))[:6]
    eventos = Evento.objects.order_by('fecha_inicio')[:3]
    form = _process_contact_form(request)
    if form is None:
        return redirect('home')
    return render(request, 'cms/home.html', {'albums': albums, 'eventos': eventos, 'contact_form': form})

def contacto(request):
    form = _process_contact_form(request)
    if form is None:
        return redirect('contacto')
    return render(request, 'cms/contacto.html', {'contact_form': form})

def galeria(request):
    album_id = request.GET.get('album')
    albums = Album.objects.filter(activo=True)
    imagenes = GaleriaImagen.objects.filter(album__activo=True).select_related('album')
    if album_id:
        imagenes = imagenes.filter(album_id=album_id)
    return render(request, 'cms/galeria.html', {'albums': albums, 'imagenes': imagenes, 'selected_album': album_id})

def institucional(request):
    return render(request, 'cms/institucional.html')

@staff_member_required
def dashboard(request):
    context = {
        'total_mensajes': ContactMessage.objects.count(),
        'mensajes_no_leidos': ContactMessage.objects.filter(atendido=False).count(),
        'mensajes_recientes': ContactMessage.objects.all()[:8],
    }
    return render(request, 'admin/dashboard.html', context)
