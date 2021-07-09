from django.urls import path
from . import views

urlpatterns = [
    # park
    path('', views.ParkList.as_view(), name='park_list'),
    path('<int:pk>/', views.ParkDetail.as_view(), name='park_detail'),
    path('create/<int:user_id>/', views.ParkCreate.as_view(), name='park_create'),
    path('update/<int:pk>/', views.ParkUpdate.as_view(), name='park_update'),
    path('delete/<int:pk>/', views.ParkDelete.as_view(), name='park_delete'),
    # park images
    path('image/', views.ParkImageList.as_view(), name='parkimage_list'),
    path('image/<int:pk>/', views.ParkImageDetail.as_view(), name='parkimage_detail'),
    path('image/create/<int:park_id>/', views.ParkImageCreate.as_view(), name='parkimage_create'),
    path('image/update/<int:pk>/', views.ParkImageUpdate.as_view(), name='parkimage_update'),
    path('image/delete/<int:pk>/', views.ParkImageDelete.as_view(), name='parkimage_delete'),
    # park other services
    path('services/', views.ParkOtherServiceList.as_view(), name='parkservices_list'),
    path('services/<int:pk>/', views.ParkOtherServiceDetail.as_view(), name='parkservices_detail'),
    path('services/create/<int:park_id>/', views.ParkOtherServiceCreate.as_view(), name='parkservices_create'),
    path('services/update/<int:pk>/', views.ParkOtherServiceUpdate.as_view(), name='parkservices_update'),
    path('services/delete/<int:pk>/', views.ParkOtherServiceDelete.as_view(), name='parkservices_delete'),
]