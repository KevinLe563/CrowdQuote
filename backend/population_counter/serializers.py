from rest_framework import serializers

from .models import Population, Location, Camera

class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = ("location_id", "people_count", "timestamp")
        lookup_field = "location_id"

    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("id", "location_id")
        lookup_field = "location_id"