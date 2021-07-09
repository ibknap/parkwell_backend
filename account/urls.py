from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserList.as_view(), name='user_list'),
    path('user/<token>/', views.UserDetail.as_view(), name='user_detail'),
    path('user/update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),

    path('register/', views.RegisterAPI.as_view(), name='register_api'),
    path('register_as_company_admin/', views.RegisterAsCompanyAdminAPI.as_view(), name='register_as_company_admin_api'),
    path('login/', views.LoginAPI.as_view(), name='login_api'),
    path('logout/', views.LogoutAPI.as_view(), name='logout_api'),

    path('company_admin_profile/', views.CompanyAdminProfileList.as_view(), name='company_admin_profile_list'),
    path('company_admin_profile/<int:pk>/', views.CompanyAdminProfileDetail.as_view(), name='company_admin_profile_detail'),
    path('company_admin_profile/create/<int:user_id>/', views.CompanyAdminProfileCreate.as_view(), name='company_admin_profile_create'),
    path('company_admin_profile/update/<int:pk>/', views.CompanyAdminProfileUpdate.as_view(), name='company_admin_profile_update'),
    path('company_admin_profile/delete/<int:pk>/', views.CompanyAdminProfileDelete.as_view(), name='company_admin_profile_delete'),

    path('park_admin_profile/', views.ParkAdminProfileList.as_view(), name='park_admin_profile_list'),
    path('park_admin_profile/<int:pk>/', views.ParkAdminProfileDetail.as_view(), name='park_admin_profile_detail'),
    path('park_admin_profile/create/<int:user_id>/<int:company_admin>/', views.ParkAdminProfileCreate.as_view(), name='park_admin_profile_create'),
    path('park_admin_profile/update/<int:pk>/', views.ParkAdminProfileUpdate.as_view(), name='park_admin_profile_update'),
    path('park_admin_profile/delete/<int:pk>/', views.ParkAdminProfileDelete.as_view(), name='park_admin_profile_delete'),
]