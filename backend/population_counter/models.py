from django.db import models
from address.models import AddressField

# Create your models here.
# Django automatically adds id/primary key field

# Location Model
class Location(models.Model):
    address = AddressField()
    building_name = models.CharField(max_length=50)

# Camera Model
class Camera(models.Model):
    # each camera must monitor 1 location
    # if location is deleted, set the location_id to null. Camera can stay in database
    location_id = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL) 

# Population Model
class Population(models.Model):
    # each population must belong to a location
    # if location is deleted, population should be deleted as well
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    people_count = models.PositiveIntegerField()
    # set timestamp to when the object is created
    timestamp = models.DateTimeField(auto_now=True)

