from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('company/', views.DashboardCompany.as_view(), name='dashboard_company'),
    path('company_detail/<int:pk>/', views.DashboardCompanyDetail.as_view(), name='dashboard_company_detail'),
    path('company_add/', views.DashboardCompanydAdd.as_view(), name='dashboard_company_add'),
    path('company_edit/<int:pk>/', views.DashboardCompanyEdit.as_view(), name='dashboard_company_edit'),
    path('company_delete/<int:pk>/', views.DashboardCompanyDelete.as_view(), name='dashboard_company_delete'),

    path('park/', views.DashboardPark.as_view(), name='dashboard_park'),
    path('park_detail/<int:pk>/', views.DashboardParkDetail.as_view(), name='dashboard_park_detail'),
    path('park_add/', views.DashboardParkdAdd.as_view(), name='dashboard_park_add'),
    path('park_edit/<int:pk>/', views.DashboardParkEdit.as_view(), name='dashboard_park_edit'),
    path('park_delete/<int:pk>/', views.DashboardParkDelete.as_view(), name='dashboard_park_delete'),

    path('check_email/<email>/', views.DashboardCheckEmail.as_view(), name='dashboard_check_email'),

    path('cadmin/', views.DashboardCompanyAdmin.as_view(), name='dashboard_cadmin'),
    path('padmin/', views.DashboardParkAdmin.as_view(), name='dashboard_padmin'),
    path('bookings/', views.DashboardBookings.as_view(), name='dashboard_bookings'),
]