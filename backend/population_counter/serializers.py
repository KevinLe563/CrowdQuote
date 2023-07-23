from rest_framework import serializers

from .models import Population, Location, Camera

class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = ("id", "people_count", "timestamp")

    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "building_name", "civic_number", "street_name", "postal_code", "longitude", "latitude")

class CameraSerializer(serializers.ModelSerializer):
    location_id = serializers.RelatedField(source='location', read_only='true')
    class Meta:
        model = Camera
        fields = ("id", "location_id")