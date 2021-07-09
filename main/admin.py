from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'id')
    search_fields = ('full_name__startswith', 'park__startswith')