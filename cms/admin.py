from django.contrib import admin
from .models import Album, ContactMessage, EmailSetting, GaleriaImagen, SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('sitio_nombre', 'logo', 'fondo_pantalla')}), ('Identidad visual', {'fields': ('color_primario_start', 'color_primario_end')}), ('Contacto', {'fields': ('email_contacto', 'telefono_contacto', 'direccion')}))
    def has_add_permission(self, request): return not SiteSetting.objects.exists()

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'ciudad', 'creado', 'estado_lectura')
    list_filter = ('atendido', 'creado')
    search_fields = ('nombre', 'email', 'asunto', 'mensaje')
    readonly_fields = ('creado',)
    actions = ('marcar_como_leidos', 'marcar_como_no_leidos')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        contact_message = self.get_object(request, object_id)
        if contact_message and not contact_message.atendido and request.method == 'GET':
            contact_message.atendido = True
            contact_message.save(update_fields=('atendido',))
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.display(description='Estado', boolean=False)
    def estado_lectura(self, obj):
        return 'Leído' if obj.atendido else 'No leído'

    @admin.action(description='Marcar mensajes como leídos')
    def marcar_como_leidos(self, request, queryset):
        queryset.update(atendido=True)

    @admin.action(description='Marcar mensajes como no leídos')
    def marcar_como_no_leidos(self, request, queryset):
        queryset.update(atendido=False)

admin.site.register([Album, GaleriaImagen])

@admin.register(EmailSetting)
class EmailSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Servidor SMTP', {'fields': ('smtp_host', 'smtp_port', 'smtp_use_tls')}),
        ('Autenticación', {'fields': ('smtp_user', 'smtp_password', 'from_email')}),
    )

    def has_add_permission(self, request):
        return not EmailSetting.objects.exists()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['smtp_password'].widget.input_type = 'password'
        return form
