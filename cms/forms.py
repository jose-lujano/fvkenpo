from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'field'

    class Meta:
        model = ContactMessage
        fields = ('nombre', 'telefono', 'email', 'edad', 'ciudad', 'mensaje')
        labels = {
            'nombre': 'Nombre completo',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
            'edad': 'Edad',
            'ciudad': 'Ciudad',
            'mensaje': 'Mensaje',
        }
        widgets = {
            'edad': forms.NumberInput(attrs={'min': 1, 'max': 120}),
            'mensaje': forms.Textarea(attrs={'rows': 5}),
        }
