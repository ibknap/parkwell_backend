from .models import Park, ParkImage, ParkOtherService
from django.contrib import admin

# park image inline in park
class ParkImageInline(admin.StackedInline):
    model = ParkImage
    extra = 4

# park other services inline in park
class ParkOtherServiceInline(admin.StackedInline):
    model = ParkOtherService
    extra = 2

@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ('park_name', 'park_email', 'company', 'id')
    search_fields = ('park_name__startswith', 'park_email__startswith', 'company__startswith', 'id__startswith',)
    inlines = [ParkImageInline, ParkOtherServiceInline]

@admin.register(ParkImage)
class ParkImageAdmin(admin.ModelAdmin):
    list_display = ('park', 'id')
    search_fields = ('park__startswith',)

@admin.register(ParkOtherService)
class ParkOtherServiceAdmin(admin.ModelAdmin):
    list_display = ('park', 'park_service', 'id')
    search_fields = ('park__startswith', 'park_service__startswith')