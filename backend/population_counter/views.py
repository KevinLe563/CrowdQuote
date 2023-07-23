from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework import views
from rest_framework.response import Response
from .serializers import PopulationSerializer, LocationSerializer, CameraSerializer
from .models import Population, Location, Camera

# Create your views here.
# class PopulationView(mixins.RetrieveModelMixin):
#     def retrieve(self, request, *args, **kwargs):
#         location_id = kwargs['']
#         return super().retrieve(request, *args, **kwargs)

class LocationLatLngView(views.APIView):
    def get(self, request, pk=None):
        lng = request.data['lng']
        lat = request.data['lat']
        try:
            location = Location.objects.all().filter(lng=lng, lat=lat).first()
            serializer = LocationSerializer(location)
            return Response(serializer.data)
        except(Location.DoesNotExist):
            print("Location doesn't exist!")


class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class CameraView(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class PopulationView(viewsets.ModelViewSet):
    queryset = Population.objects.all()
    serializer_class = PopulationSerializer

