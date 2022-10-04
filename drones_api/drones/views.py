from tokenize import String
from django.http.response import JsonResponse
from django.http import QueryDict
from .models import Model, State, Image, Drone, Medication
from .serializers import DroneSerializer, MedicationSerializer
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
import re
import logging
import datetime 


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
        if not re.search("^[a-zA-Z0-9]*$", droneSerializer.initial_data['serialNumber']):
                return JsonResponse({'message': 'Invalid Drone serial number'}, status=status.HTTP_406_NOT_ACCEPTABLE)
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
        if not drone.batteryCapacity >= 25 or drone.state.id != 1:
            stateName = State.objects.get(id=1)
            return JsonResponse({'message': "The drone is not available for loading. Battery is on: "+ str(drone.batteryCapacity) + " and State is: " + stateName.value}, status=status.HTTP_400_BAD_REQUEST)
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
        droneAvailableWeight = drone.weightLimit
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
                droneAvailableWeight-=medication.weight
                if droneAvailableWeight >= 0:
                    medication.drone = drone
                    medication.save()
                else:
                    break
            except Medication.DoesNotExist:
                medicationNotFound+=1 
                continue
        if not medication:
            message = "No medications found"
        else:
            message = "Medications successfully loaded into Drone. "
            if medicationNotFound > 0:
                message += "At least one medication wasn't found. "
            if not droneAvailableWeight >= 0:
                message += "At least one medication wasn't loaded due to drone's weight limit."
        return JsonResponse({'message': message }, status=status.HTTP_200_OK)
    except Drone.DoesNotExist: 
        return JsonResponse({'message': 'The Drone does not exist'}, status=status.HTTP_404_NOT_FOUND)     

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def checkingLoadedDroneView(request, pk = None, serialNumber = None):
    try:         
        if pk is not None:
            drone = Drone.objects.get(pk=pk)
        else: 
            drone = Drone.objects.get(serialNumber=serialNumber)       
        #Check for medications loaded in the Drone
        queryset = Medication.objects.filter(drone=drone)
        medicationSerializer = MedicationSerializer(queryset, many=True)
        if len(medicationSerializer.data) > 0:
            return JsonResponse(medicationSerializer.data, safe=False)
        else:
            return JsonResponse({'message': 'No medications loaded for the given drone'}, status=status.HTTP_404_NOT_FOUND)
    except Drone.DoesNotExist: 
        return JsonResponse({'message': 'The Drone does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def checkingAvailableDronesView(request):
    try:        
        #Check for Drones in Idle and Battery >= than 25
        queryset = Drone.objects.filter(state=1).filter(batteryCapacity__gte=25)
        droneSerializer = DroneSerializer(queryset, many=True)
        if len(droneSerializer.data) > 0:
            return JsonResponse(droneSerializer.data, safe=False)
        else:
            return JsonResponse({'message': 'No drones available for load'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def checkingDronesBatteryView(request, pk = None, serialNumber = None):    
    try:        
        if pk is not None:
            drone = Drone.objects.get(pk=pk)
        else: 
            drone = Drone.objects.get(serialNumber=serialNumber)    
        return JsonResponse({'message': 'The drone has ' + str(drone.batteryCapacity) +'% battery capacity'})
            
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

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def medicationDetailView(request, pk = None, name = None, code = None):
    try: 
        if pk is not None:
            medication = Medication.objects.get(pk=pk)
        elif name is not None: 
            medication = Medication.objects.get(name=name)
        else:
            medication = Medication.objects.get(code=code)
    except Medication.DoesNotExist: 
        return JsonResponse({'message': 'The Medication does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        medicationSerializer = MedicationSerializer(medication) 
        return JsonResponse(medicationSerializer.data) 
 
    elif request.method == 'PUT' or request.method == 'PATCH':
        medicationData = JSONParser().parse(request) 
        medicationSerializer = MedicationSerializer(medication, data=medicationData) 
        if medicationSerializer.is_valid():
            if not re.search("^[a-zA-Z0-9_-]*$", medicationSerializer.initial_data['name']):
                return JsonResponse({'message': 'Invalid Medication Name'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if not re.search("^[A-Z0-9_]*$", medicationSerializer.initial_data['code']):
                return JsonResponse({'message': 'Invalid Medication Code'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
            medicationSerializer.save() 
            return JsonResponse(medicationSerializer.data) 
        return JsonResponse(medicationSerializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        medication.delete() 
        return JsonResponse({'message': 'Medication was deleted successfully!'}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def createAuditLog(request):
    logger = logging.getLogger('audit_logger')    
    queryset = Drone.objects.all()      
    droneSerializer = DroneSerializer(queryset, many=True)
    checkDateTime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")    
    checkTime = datetime.datetime.now().strftime("%H:%M:%S")
    logger.warning('\n' + checkDateTime +' - Initializing full Battery Check')
    if not len(droneSerializer.data) > 0:
        logger.warning(checkTime + ' - No Drones available for battery check!')
        return JsonResponse({"message":"No Drones available for battery check!"})
    for drone in droneSerializer.data:
        logger.warning(checkTime +' - Drone #' + str(drone.get('id')) + ' with Serial Number: ' + str(drone.get('serialNumber')) + '. Battery Capacity on: ' + str(drone.get('batteryCapacity')) + '%.' )    
    return JsonResponse({"message":"All battery drones were successfully checked!"})