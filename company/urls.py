from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyList.as_view(), name='company_list'),
    path('<int:pk>/', views.CompanyDetail.as_view(), name='company_detail'),
    path('create/<int:user_id>/', views.CompanyCreate.as_view(), name='company_create'),
    path('update/<int:pk>/', views.CompanyUpdate.as_view(), name='company_update'),
    path('delete/<int:pk>/', views.CompanyDelete.as_view(), name='company_delete'),
]