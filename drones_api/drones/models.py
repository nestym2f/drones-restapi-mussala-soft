from audioop import minmax
from os import name
from pyexpat import model
from re import M
from django.db import models


class Model(models.Model):
    value = models.CharField(max_length=15)
class State(models.Model):
    value = models.CharField(max_length=12)
class Image(models.Model):
    url = models.CharField(max_length=255)
class Drone(models.Model):
    serialNumber = models.CharField(max_length=100, db_column='serial_number')
    model = models.ForeignKey(Model,null=True, on_delete=models.SET_NULL)
    weightLimit = models.DecimalField(default=0.1, max_digits=5, decimal_places=2, db_column='weight_limit')
    batteryCapacity = models.PositiveSmallIntegerField(default=0, db_column='battery_capacity')
    state = models.ForeignKey(State,null=True, on_delete=models.SET_NULL)    
class Medication(models.Model):
    name = models.CharField(max_length=255)
    weight = models.DecimalField(default=0.1, max_digits=5, decimal_places=2)
    code = models.CharField(max_length=255);
    image = models.ForeignKey(Image, on_delete=models.CASCADE)