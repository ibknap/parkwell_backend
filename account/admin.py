from .models import Administrator
from django.contrib import admin

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification', 'is_company_admin', 'is_park_admin', 'mobile_number', 'id')
    search_fields = ('user__startswith', 'mobile_number__startswith', 'id__startswith',)