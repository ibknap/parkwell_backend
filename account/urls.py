from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user/control/<int:id>/', views.UserControl.as_view(), name='user_control'),
    path('user/update_firstname/', views.UpdateFirstName.as_view(), name='update_first_name'),
    path('user/update_lastname/', views.UpdateLastName.as_view(), name='update_last_name'),

    path('register/', views.Register.as_view(), name='register'),
    path('admin_register/', views.AdminRegister.as_view(), name='admin_register'),
    path('login/', views.Login.as_view(), name='login'),
    path('admin_login/', views.AdminLogin.as_view(), name='admin_login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('verify_email/<uidb64>/<token>/', views.VerifyEmail.as_view(), name='verify_email'),
]