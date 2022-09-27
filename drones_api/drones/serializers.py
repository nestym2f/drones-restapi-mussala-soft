from rest_framework import serializers
from .models import Model, State, Image, Drone, Medication

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ["id", "value"]
        
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "value"]

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url"]
        
class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ["id", "serialNumber", "model", "weightLimit", "batteryCapacity", "state"]

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["id", "name", "weight", "code", "image", "drone"]