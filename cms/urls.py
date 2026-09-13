from django.urls import path
from .views import contacto, dashboard, galeria, home, institucional
urlpatterns = [
    path('', home, name='home'),
    path('institucional/', institucional, name='institucional'),
    path('galeria/', galeria, name='galeria'),
    path('contacto/', contacto, name='contacto'),
    path('admin/dashboard/', dashboard, name='admin_dashboard'),
]