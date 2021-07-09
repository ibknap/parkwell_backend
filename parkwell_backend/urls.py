from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from main import api_services

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path(f'api/v{api_services.api_version()}/account/', include('account.urls')),
    path(f'api/v{api_services.api_version()}/company/', include('company.urls')),
    path(f'api/v{api_services.api_version()}/dashboard/', include('dashboard.urls')),
    path('', include('main.urls')),
    path(f'api/v{api_services.api_version()}/map/', include('map.urls')),
    path(f'api/v{api_services.api_version()}/park/', include('park.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)