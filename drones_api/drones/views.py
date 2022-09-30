from django.http.response import JsonResponse
from django.http import QueryDict
from .models import Model, State, Image, Drone, Medication
from .serializers import DroneSerializer, MedicationSerializer
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
import re

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
        if float(droneSerializer.initial_data['weightLimit']) > 500 or float(droneSerializer.initial_data['weightLimit']) < 0:
            return JsonResponse({'message': 'Invalid Weight Limit, weight limit must be 0 >= 500 '}, status=status.HTTP_406_NOT_ACCEPTABLE) 
        droneSerializer.save()
        return JsonResponse(droneSerializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(droneSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def dronesDeleteAllView(request):    
    count = Drone.objects.all().delete()        
    return JsonResponse({'message': '{} Drones were deleted successfully!'.format(count[0])}, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def droneDetailView(request, pk = None, serialNumber = None):
    try: 
        if pk is not None:
            drone = Drone.objects.get(pk=pk)
        else: 
            drone = Drone.objects.get(serialNumber=serialNumber)
    except Drone.DoesNotExist: 
        return JsonResponse({'message': 'The Drone does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        droneSerializer = DroneSerializer(drone) 
        return JsonResponse(droneSerializer.data) 
 
    elif request.method == 'PUT' or request.method == 'PATCH':
        droneData = JSONParser().parse(request) 
        droneSerializer = DroneSerializer(drone, data=droneData) 
        if droneSerializer.is_valid():
            if int(droneSerializer.initial_data['batteryCapacity']) < 25 and droneSerializer.initial_data['state'] == "2":
                return JsonResponse({'message': 'Can not Update a Drone to Loading State with less that 25% Battery'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
            if int(droneSerializer.initial_data['batteryCapacity']) > 100 or int(droneSerializer.initial_data['batteryCapacity']) < 0:
                return JsonResponse({'message': 'Invalid Battery Capacity, battery capacity must be 0 >= 100'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
            if float(droneSerializer.initial_data['weightLimit']) > 500 or float(droneSerializer.initial_data['weightLimit']) < 0:
                return JsonResponse({'message': 'Invalid Weight Limit, weight limit must be 0 >= 500 '}, status=status.HTTP_406_NOT_ACCEPTABLE) 
            droneSerializer.save() 
            return JsonResponse(droneSerializer.data) 
        return JsonResponse(droneSerializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        drone.delete() 
        return JsonResponse({'message': 'Drone was deleted successfully!'}, status=status.HTTP_200_OK)
    
@api_view(['PATCH'])
@permission_classes((permissions.AllowAny,))
def droneLoadMedicationsView(request, pk = None, serialNumber = None):
    try: 
        #Check for Drone
        if pk is not None:
            drone = Drone.objects.get(pk=pk)
        else: 
            drone = Drone.objects.get(serialNumber=serialNumber)
        #Check is Json data is valid
        if not request.data.get('searchMedicationBy'):
            return JsonResponse({'message': "Not valid request, searchMedicationBy i empty or isn't present"}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('medicationValue'):
            return JsonResponse({'message': "Not valid request, medicationValue is empty or isn't present"}, status=status.HTTP_400_BAD_REQUEST)                
        searchMedicationBy = request.data.get('searchMedicationBy')        
        medicationValue = request.data.get('medicationValue')
        #Check for old medications loaded in the Drone to empty
        medicationsLoaded = Medication.objects.filter(drone=drone)
        if medicationsLoaded.count() > 0:
            for medLoaded in medicationsLoaded:
                medLoaded.drone = None
                medLoaded.save()                
        #Check for id, code or name of medications to load into the Drone
        medication = None
        medicationNotFound = 0
        message = ''
        for medVal in medicationValue:
            try:
                if searchMedicationBy == 'id':
                    medication = Medication.objects.get(id=medVal)                
                elif searchMedicationBy == 'code':
                    medication = Medication.objects.get(code=medVal)                
                elif searchMedicationBy == 'name':
                    medication = Medication.objects.get(name=medVal)                
                medication.drone = drone
                medication.save()
            except Medication.DoesNotExist:
                medicationNotFound+=1 
                continue
        if not medication:
            message = "No medications found"
        else:
            message = "Medications successfully loaded into Drone. "
            if medicationNotFound > 0:
                message += "At least one medication wasn't found"     
        return JsonResponse({'message': message }, status=status.HTTP_200_OK)
    except Drone.DoesNotExist: 
        return JsonResponse({'message': 'The Drone does not exist'}, status=status.HTTP_404_NOT_FOUND)     

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def medicationGetAllView(request):    
    queryset = Medication.objects.all()        
    medicationSerializer = MedicationSerializer(queryset, many=True)
    return JsonResponse(medicationSerializer.data, safe=False)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def medicationRegisterView(request):     
    medicationData = JSONParser().parse(request)
    medicationSerializer = MedicationSerializer(data=medicationData)    
        
    if medicationSerializer.is_valid():        
        if not re.search("^[a-zA-Z0-9_-]*$", medicationSerializer.initial_data['name']):
            return JsonResponse({'message': 'Invalid Medication Name'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if not re.search("^[A-Z0-9_]*$", medicationSerializer.initial_data['code']):
            return JsonResponse({'message': 'Invalid Medication Code'}, status=status.HTTP_406_NOT_ACCEPTABLE)        
        medicationSerializer.save()
        return JsonResponse(medicationSerializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(medicationSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def medicationDeleteAllView(request):    
    count = Medication.objects.all().delete()        
    return JsonResponse({'message': '{} Medications were deleted successfully!'.format(count[0])}, status=status.HTTP_200_OK)
