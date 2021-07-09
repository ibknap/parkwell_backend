from .models import CompanyAdminProfile, ParkAdminProfile
from django.contrib import admin

@admin.register(CompanyAdminProfile)
class CompanyAdminProfileAdmin(admin.ModelAdmin):
    list_display = ('admin', 'company_admin_number', 'id')
    search_fields = ('admin__startswith', 'company_admin_number__startswith', 'id__startswith',)

@admin.register(ParkAdminProfile)
class ParkAdminProfileAdmin(admin.ModelAdmin):
    list_display = ('admin', 'park_admin_number', 'id')
    search_fields = ('admin__startswith', 'park_admin_number__startswith', 'id__startswith',)