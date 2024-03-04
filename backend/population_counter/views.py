import json

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from .serializers import PopulationSerializer, LocationSerializer, CameraSerializer
from .models import Population, Location, Camera
from .hierarchical_clustering import hierarchical_cluster

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

    def put(self, request):
        obj = Location.objects.all().filter(id=request.query_params['id']).first()
        if not obj:
            return Response(
                {"res": "Object with location id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "id": request.query_params['id'],
            "civic_number": request.data.get('civic_number'),
            "street_name": request.data.get('street_name'),
            "postal_code": request.data.get('postal_code'),
            "building_name": request.data.get('building_name'),
            "room": request.data.get('room'),
            "lng": request.data.get('lng'),
            "lat": request.data.get('lat'), 
        }
        serializer = LocationSerializer(instance=obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CameraView(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class PopulationView(views.APIView):
    def post(self, request, format=None):
        # request.data
        # process
        # replace the field in the data with updted data -> output of clustering will be {cluster #: ["x,y", "x,y"]}
        best_k, best_cluster = hierarchical_cluster(json.loads(request.data["grid"]))
        request.data["grid"] = best_cluster
        serializer = PopulationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # return population in the last 72 hours
        location_id = request.query_params["location_id"]
        qs = Population.objects.filter(location_id=location_id, timestamp__gte=timezone.now()-timezone.timedelta(days=1)).order_by("timestamp")
        serializer = PopulationSerializer(qs, many=True)
        return Response(serializer.data)

