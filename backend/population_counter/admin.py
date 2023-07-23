from django.contrib import admin

# Register your models here.
from .models import Location, Camera, Population

class LocationAdmin(admin.ModelAdmin):
    list_display = ("building_name", "civic_number", "street_name", "postal_code", "lng", "lat")

admin.site.register(Location, LocationAdmin)