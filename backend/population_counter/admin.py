from django.contrib import admin

# Register your models here.
from .models import Location, Camera, Population

class LocationAdmin(admin.ModelAdmin):
    list_display = ("building_name", "address")

admin.site.register(Location, LocationAdmin)