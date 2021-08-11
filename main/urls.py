from django.urls import path
from . import views

urlpatterns = [
    path('', views.Main.as_view(), name="main"),
    path('waitlist/', views.Waitlist.as_view(), name="waitlist"),
    path('navigate/<park_id>/<coord_lat>/<coord_lon>/', views.NavigateView.as_view(), name="navigate"),

    path('contact_us/', views.ContactUs.as_view(), name='contact_us'),
    
    path("search_autocomplete/", views.SearchAutocomplete.as_view(), name="search_autocomplete"),
    path("search/", views.Search.as_view(), name="search_page"),

    path('booking/create/<int:pk>/', views.Booking.as_view(), name='booking'),
    path('booking/<int:pk>/', views.BookingDetail.as_view(), name='booking_detail'),
    path('booking/control/<int:park_id>/<int:id>/', views.BookingControl.as_view(), name='booking_control'),
]
