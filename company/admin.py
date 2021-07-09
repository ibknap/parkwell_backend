from django.contrib import admin
from park.models import Park
from .models import Company

# park inline in company
class ParkInline(admin.StackedInline):
    model = Park
    extra = 1

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_email', 'admin', 'id')
    search_fields = ('company_name__startswith', 'company_email__startswith', 'admin__startswith', 'id__startswith',)
    inlines = [ParkInline]