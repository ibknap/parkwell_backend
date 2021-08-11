from .models import Administrator, ParkAdmin
from django.contrib import admin

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification', 'is_company_admin', 'mobile_number', 'id')
    search_fields = ('user__startswith', 'mobile_number__startswith', 'id__startswith',)

@admin.register(ParkAdmin)
class ParkAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_admin', 'mobile_number', 'id')
    search_fields = ('user__startswith', 'company_admin__startswith', 'mobile_number__startswith', 'id__startswith',)