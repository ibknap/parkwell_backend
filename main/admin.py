from .models import Booking, Navigate
from django.contrib import admin

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'id')
    search_fields = ('full_name__startswith', 'park__startswith')

@admin.register(Navigate)
class NavigateAdmin(admin.ModelAdmin):
    list_display = ('park', 'id')
    search_fields = ('park__startswith', 'id__startswith')