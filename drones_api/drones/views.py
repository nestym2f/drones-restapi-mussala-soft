from ast import parse
from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Model, State, Image, Drone, Medication
from .serializers import DroneSerializer, MedicationSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
    
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def dronesGetAllView(request):    
    queryset = Drone.objects.all()        
    droneSerializer = DroneSerializer(queryset, many=True)
    return JsonResponse(droneSerializer.data, safe=False)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def dronesRegisterView(request):
    if Drone.objects.all().count() >= 10:
        return JsonResponse({'message': 'Already 10 drones on DB, unable to insert more drones'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
    droneData = JSONParser().parse(request)
    droneSerializer = DroneSerializer(data=droneData)
    if droneSerializer.is_valid():
        if int(droneSerializer.initial_data['batteryCapacity']) < 25 and droneSerializer.initial_data['state'] == "2":
            return JsonResponse({'message': 'Can not register a Drone with less that 25% Battery and Loading State'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
        if int(droneSerializer.initial_data['batteryCapacity']) > 100 or int(droneSerializer.initial_data['batteryCapacity']) < 0:
            return JsonResponse({'message': 'Invalid Battery Capacity, battery capacity must be 0 >= 100'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
        if int(droneSerializer.initial_data['weightLimit']) > 500 or int(droneSerializer.initial_data['weightLimit']) < 0:
            return JsonResponse({'message': 'Invalid Weight Limit, weight limit must be 0 >= 500 '}, status=status.HTTP_406_NOT_ACCEPTABLE) 
        droneSerializer.save()
        return JsonResponse(droneSerializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(droneSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def dronesDeleteAllView(request):    
    count = Drone.objects.all().delete()        
    return JsonResponse({'message': '{} Drones were deleted successfully!'.format(count[0])}, status=status.HTTP_200_OK)