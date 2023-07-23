from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .serializers import PopulationSerializer, LocationSerializer, CameraSerializer
from .models import Population, Location, Camera

# Create your views here.
# class PopulationView(mixins.RetrieveModelMixin):
#     def retrieve(self, request, *args, **kwargs):
#         location_id = kwargs['']
#         return super().retrieve(request, *args, **kwargs)

class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class CameraView(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

