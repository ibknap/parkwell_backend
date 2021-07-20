from main import api_services
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Main.as_view(), name="main"),
    path('docs/', views.Docs.as_view(), name="docs"),
    path('notify/', views.Notify.as_view(), name="notify"),

    path(f'api/v{api_services.api_version()}/contact_us/', views.ContactUsAPI.as_view(), name='contact_us'),
    
    path(f"api/v{api_services.api_version()}/search_autocomplete/", views.SearchAutocomplete.as_view(), name="search_autocomplete"),
    path(f"api/v{api_services.api_version()}/search/", views.Search.as_view(), name="search_page"),

    path(f'api/v{api_services.api_version()}/booking/', views.BookingList.as_view(), name='booking_list'),
    path(f'api/v{api_services.api_version()}/booking/<int:pk>/', views.BookingDetail.as_view(), name='booking_detail'),
    path(f'api/v{api_services.api_version()}/booking/create/<int:park_id>/', views.BookingCreate.as_view(), name='booking_create'),
    path(f'api/v{api_services.api_version()}/booking/update/<int:pk>/', views.BookingUpdate.as_view(), name='booking_update'),
    path(f'api/v{api_services.api_version()}/booking/delete/<int:pk>/', views.BookingDelete.as_view(), name='booking_delete'),
]
