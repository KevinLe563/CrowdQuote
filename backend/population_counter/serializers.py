from rest_framework import serializers

from .models import Population, Location

class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = ("people_count", "timestamp")

    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("building_name", "civic_number", "street_name", "postal_code")