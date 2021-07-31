from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from account import views

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('company/', include('company.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('main.urls')),
    path('map/', include('map.urls')),
    path('park/', include('park.urls')),

    # password reset and blocking some paths
    path('accounts/', views.Login.as_view()),
    path('accounts/login/', views.Login.as_view()),
    path('accounts/logout/', views.Logout.as_view()),
    path('accounts/password_change/', views.Login.as_view()),
    path('accounts/password_change/done/', views.Login.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
]

# handling page errors
handler403 = 'main.views.error_403'
handler400 = 'main.views.error_400'
handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)