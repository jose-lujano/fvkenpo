from django.contrib import admin
from .models import Asociacion, Club, Atleta, Arbitro
admin.site.register([Asociacion, Club, Atleta, Arbitro])