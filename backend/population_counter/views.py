from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from .serializers import PopulationSerializer, LocationSerializer, CameraSerializer
from .models import Population, Location, Camera

# Create your views here.
# class PopulationView(mixins.RetrieveModelMixin):
#     def retrieve(self, request, *args, **kwargs):
#         location_id = kwargs['']
#         return super().retrieve(request, *args, **kwargs)

class LocationView(views.APIView):
    def get(self, request, pk=None):
        print(request.query_params)
        lng = request.query_params['lng']
        lat = request.query_params['lat']
        try:
            qs = Location.objects.all().filter(lng=lng, lat=lat).first()
            serializer = LocationSerializer(qs)
            return Response(serializer.data)
        except(Location.DoesNotExist):
            print("Location doesn't exist!")

class CameraView(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class PopulationView(views.APIView):
    def post(self, request, format=None):
        serializer = PopulationSerializer(data=request.query_params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # return population in the last 72 hours
        location_id = request.query_params["location_id"]
        qs = Population.objects.filter(location_id=location_id, timestamp__gte=timezone.now()-timezone.timedelta(days=3)).order_by("timestamp")
        serializer = PopulationSerializer(qs, many=True)
        return Response(serializer.data)

