import json
from drones import views
from rest_framework import status
from rest_framework.test import APITestCase


"""    
    
    url(r'^api/create-battery-log', views.createAuditLog, name='drones-battery-log'),
"""
#--------------------------------------------Medications-----------------------------------------------------#

class MedicationRegisterViewTestCase(APITestCase):
    def test_register_medication(self):
        jsonObject = {"name": "Med_name","weight":"150","image": "1","code":"MED_CODE"}                         
        response = self.client.post("/api/medications/register",data=json.dumps(jsonObject),content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class MedicationGetAllViewTestCase(APITestCase):
    def test_get_all_medications(self):
        response = self.client.get("/api/medications/")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')        
        
class MedicationDeleteAllViewTestCase(APITestCase):
    def test_delete_all_medications(self):
        response = self.client.delete("/api/medications/delete")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class MedicationDetailsViewTestCase(APITestCase):    
        
    def test_get_medications_by_id(self):
        response = self.client.get("/api/medications/id/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')
        
    def test_get_medications_by_name(self):
        response = self.client.get("/api/medications/name/amoxicilin_250mg")    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')
        
    def test_get_medications_by_code(self):
        response = self.client.get("/api/medications/code/AMXCL_250")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')
    
    def test_delete_medications_by_id(self):
        response = self.client.delete("/api/medications/id/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')
        self.assertEqual(json.loads(response.content)['message'],"Medication was deleted successfully!")
        
    def test_delete_medications_by_name(self):
        response = self.client.delete("/api/medications/name/amoxicilin_250mg")    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')
        self.assertEqual(json.loads(response.content)['message'],"Medication was deleted successfully!")
        
    def test_delete_medications_by_code(self):
        response = self.client.delete("/api/medications/code/AMXCL_250")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')
        self.assertEqual(json.loads(response.content)['message'],"Medication was deleted successfully!")
        
    def test_update_medications_by_id(self):
        jsonObject = {"name": "Med_name_UPDATE","weight":"180","image": "1","code":"MED_CODE_UPDATE"}
        response = self.client.put("/api/medications/id/1",data=json.dumps(jsonObject),content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')
        self.assertEqual(json.loads(response.content)['id'],1)
        
    def test_update_medications_by_name(self):
        jsonObject = {"name": "Med_name_UPDATE","weight":"180","image": "1","code":"MED_CODE_UPDATE"}
        response = self.client.put("/api/medications/name/amoxicilin_250mg",data=json.dumps(jsonObject),content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'name')
        self.assertEqual(json.loads(response.content)['name'],"Med_name_UPDATE")
        
    def test_update_medications_by_code(self):
        jsonObject = {"name": "Med_name_UPDATE","weight":"180","image": "1","code":"MED_CODE_UPDATE"}
        response = self.client.put("/api/medications/code/AMXCL_250",data=json.dumps(jsonObject),content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'code')
        self.assertEqual(json.loads(response.content)['code'],"MED_CODE_UPDATE")
        
#--------------------------------------------Drones-----------------------------------------------------#
class DroneRegisterViewTestCase(APITestCase):
    def test_register_drone(self):
        jsonObject = {"serialNumber": "123456aM7890","weightLimit":"500","batteryCapacity": "100","model":"4","state":"1"}
        response = self.client.post("/api/drones/register",data=json.dumps(jsonObject),content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
class DroneGetAllViewTestCase(APITestCase):
    def test_get_all_drones(self):
        response = self.client.get("/api/drones/")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')        
        
class DroneDeleteAllViewTestCase(APITestCase):
    def test_delete_all_drones(self):
        response = self.client.delete("/api/drones/delete")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class DroneDetailsViewTestCase(APITestCase):    
        
    def test_get_drone_by_id(self):
        response = self.client.get("/api/drones/id/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')
        
    def test_get_drone_by_serial_number(self):
        response = self.client.get("/api/drones/serial-number/1111222333444")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')        
    
    def test_delete_drone_by_id(self):
        response = self.client.delete("/api/drones/id/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')
        self.assertEqual(json.loads(response.content)['message'],"Drone was deleted successfully!")
        
    def test_delete_by_serial_number(self):
        response = self.client.delete("/api/drones/serial-number/1111222333444")    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')
        self.assertEqual(json.loads(response.content)['message'],"Drone was deleted successfully!")
        
    def test_update_drone_by_id(self):
        jsonObject = {"serialNumber": "12EMFF56aM7890","weightLimit":"450","batteryCapacity": "95","model":"4","state":"3"}
        response = self.client.put("/api/drones/id/1",data=json.dumps(jsonObject),content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')
        self.assertEqual(json.loads(response.content)['id'],1)
        
    def test_update_drone_by_serial_number(self):
        jsonObject = {"serialNumber": "12EMFF56aM7890","weightLimit":"450","batteryCapacity": "95","model":"4","state":"3"}
        response = self.client.put("/api/drones/serial-number/1111222333444",data=json.dumps(jsonObject),content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'name')
        self.assertEqual(json.loads(response.content)['serialNumber'],"12EMFF56aM7890")

class DroneLoadMedicationViewTestCase(APITestCase):

    def test_drone_load_medication_by_id(self):
        jsonObject={"searchMedicationBy": "id", "medicationValue": ["1","2","3"]}         
        response = self.client.patch("/api/drones/load-medications/id/6",data=json.dumps(jsonObject),content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')
        message = json.loads(response.content)['message']
        self.assertRegex(message, r'^Medications successfully loaded into Drone.')        
        
        
    def test_drone_load_medication_by_serial_number(self):
        jsonObject={"searchMedicationBy": "id", "medicationValue": ["1","2","3"]} 
        response = self.client.patch("/api/drones/load-medications/serial-number/2222333652377",data=json.dumps(jsonObject),content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')
        message = json.loads(response.content)['message']
        self.assertRegex(message, r'^Medications successfully loaded into Drone.')

class DroneCheckingAvailableTestCase(APITestCase):
    def test_get_available_drones(self):
        response = self.client.get("/api/drones/available-to-load/")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'id')     

class DroneCheckingBatteryTestCase(APITestCase):
    def test_check_battery_by_id(self):
        response = self.client.get("/api/drones/check-battery-capacity/id/1")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')
        message = json.loads(response.content)['message']
        self.assertRegex(message, r'battery capacity')
        
    
    def test_check_battery_by_serial_number(self):
        response = self.client.get("/api/drones/check-battery-capacity/serial-number/1111222333444")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')
        message = json.loads(response.content)['message']
        self.assertRegex(message, r'battery capacity')

#--------------------------------------------Log-----------------------------------------------------#
class CreateBatteryLogTestCase(APITestCase):
    def test_create_battery_log(self):
        response = self.client.get("/api/create-battery-log")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(response['content-type'], 'application/json')
        self.assertTrue(response,'message')        
        self.assertEqual(json.loads(response.content)['message'],"All battery drones were successfully checked!")       
        

