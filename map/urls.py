from django.urls import path
from . import views

urlpatterns = [
    path('<str:search>/', views.Map.as_view(), name='map'),
]