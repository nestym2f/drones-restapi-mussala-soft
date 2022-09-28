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



@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def dronesDeleteAllView(request):    
    count = Drone.objects.all().delete()        
    return JsonResponse({'message': '{} Drones were deleted successfully!'.format(count[0])}, status=status.HTTP_200_OK)