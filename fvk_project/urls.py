from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from cms.views import dashboard

urlpatterns = [
    path('admin/dashboard/', dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
    path('deporte/', include('deporte.urls')),
    path('competencia/', include('competencia.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
