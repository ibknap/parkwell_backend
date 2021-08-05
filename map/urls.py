from django.urls import path
from . import views

urlpatterns = [
    path('<lon>,<lat>/', views.Map.as_view(), name='map'),
]