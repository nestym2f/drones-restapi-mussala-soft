## REQUIREMENTS
- Python 3.6 ≥ 3.10
- Django 3.2 ≥ 4.0
- Django Rest Framework 3.14.0
- Git ≥ 2.30
- django-cors-headers 3.13.0
- virtualenv package 

## INSTALLATION
- Install Python 3.6 ≥ 3.10
- Install Git ≥ 2.30
### Create the project directory
#### type and run in a console
- mkdir `directory-name`
- cd `directory-name`
- git init
- git remote add origin https://github.com/nestym2f/drones-restapi-mussala-soft.git
- git pull origin master

## BUILD AND RUN
#### Create a virtual environment to isolate packages dependencies for the project
#### type and run in a console
- pip install virtualenv
- python3 virtualenv `environment-name`
- source `environment-name`/bin/activate ***On Windows use*** `environment-name`\Scripts\activate
- pip install -r requirements.txt
- cd drones_api
- python manage.py runserver 8080

***The*** `runserver 8080` ***command will start a local server with ip:port 127.0.0.1:8080, every endpoint full url below should be:***
```
ex: http://127.0.0.1:8080/api/drones/
ex: http://127.0.0.1:8080/api/drones/id/5
ex: http://127.0.0.1:8080/api/medications/id/5
```
## ENDPOINTS

***Get drones list*** `(method=GET)`
```
/api/drones/ 
```
***Delete all drones*** `(method=DELETE)`
```
/api/drones/delete
```
***Register new drone*** `(method=POST)`

`The drone serial number only allows numbers and letters`
```
/api/drones/register
```
```
payload={"serialNumber":string [a-zA-Z0-9]{1,100}, "weightLimit":double, "batteryCapacity":integer, "model":string ["1","2","3","4"]}
ex: payload={
    "serialNumber": "123456aM7890",
    "weightLimit":"500",
    "batteryCapacity": "100",
    "model":"4",
    "state":"1"
}
```
***Get/Update/Delete drone by ID*** `(method=GET,PATCH,PUT,DELETE)`
```
/api/drones/id/<id>
```
```
only for PUT and PATCH
payload={"serialNumber":string [a-zA-Z0-9]{1,100}, "weightLimit":double, "batteryCapacity":integer, "model":string ["1","2","3","4"]}
ex: payload={
    "serialNumber": "123456aM7895",
    "weightLimit": "500",
    "batteryCapacity": 95,
    "model": 4,
    "state": 2
}
```
***Get/Update/Delete drone by Serial Number*** `(method=GET,PATCH,PUT,DELETE)`
```
/api/drones/serial-number/<serial-number>
```
```
only for PUT and PATCH
payload={"serialNumber":string [a-zA-Z0-9]{1,100}, "weightLimit":double, "batteryCapacity":integer, "model":string ["1","2","3","4"]}
ex: payload={
    "serialNumber": "123456aM7895",
    "weightLimit": "500",
    "batteryCapacity": 95,
    "model": 4,
    "state": 2
}
```
***Load drone by ID*** `(method=PATCH)`

`Are available to load only drones with IDLE state and Battery >= 25`
```
/api/drones/load-medications/id/<id>
```
```
payload={"searchMedicationBy": "string", "medicationValue": array["string"]}
ex: payload={"searchMedicationBy": "id", "medicationValue": ["1","2","3"]} 
ex: payload={"searchMedicationBy": "code", "medicationValue": "AMXCL_250"}
ex: payload={"searchMedicationBy": "name", "medicationValue": ["amoxicilin_250mg","MO_TABLET_200"] }
```
***Load drone by Serial Number*** `(method=PATCH)`

`Are available to load only drones with IDLE state and Battery >= 25`
```
/api/drones/load-medications/serial-number/<serial-number>
```
```
payload={"searchMedicationBy": "string", "medicationValue": array["string"]}
ex: payload={"searchMedicationBy": "id", "medicationValue": ["1","2","3"]} 
ex: payload={"searchMedicationBy": "code", "medicationValue": "AMXCL_250"}
ex: payload={"searchMedicationBy": "name", "medicationValue": ["amoxicilin_250mg","MO_TABLET_200"] }
``` 
***Check load medications by drone Serial Number*** `(method=GET)`
```
/api/drones/check-loaded-medications/serial-number/<serial-number>
```
***Check load medications by drone ID*** `(method=GET)`
```
/api/drones/check-loaded-medications/id/<id>
```
***Check Drones Available to Load*** `(method=GET)`

`Are available those drones with IDLE state and Battery >= 25`
```
/api/drones/available-to-load
```
***Check Battery Capacity by drone Serial Number*** `(method=GET)`
```
api/drones/check-battery-capacity/serial-number/<serial-number>
```
***Check Battery Capacity by drone ID*** `(method=GET)`
```
api/drones/check-battery-capacity/id/<id>
```

***Get medications list*** `(method=GET)`
```
/api/medications/ 
```
***Delete all medications*** `(method=DELETE)`
```
/api/medications/delete
```
***Register new medication*** `(method=POST)`

`"image" represents the id of the image`
```
/api/medications/register
```
```
payload={"name":string [a-zA-Z0-9_-], "weight":double,"image":int,"code":string [A-Z0-9_]
}
ex: payload={
    "name": "Med_name",
    "weight":"180",
    "image": "1",
    "code":"MED_CODE"
}
```
***Get/Update/Delete medication by Id*** `(method=GET,PATCH,PUT,DELETE)`
```
/api/medications/id/<id>

```
```
only for PUT and PATCH
payload={"name":string [a-zA-Z0-9_-], "weight":double,"image":int,"code":string [A-Z0-9_]
}
ex: payload={
    "name": "NEW_NAME",
    "weight":"154",
    "image": "2",
    "code":"NEW_CODE"
}
```
***Get/Update/Delete medication by name*** `(method=GET,PATCH,PUT,DELETE)`
```
/api/medications/name/<name>
```
```
only for PUT and PATCH
payload={"name":string [a-zA-Z0-9_-], "weight":double,"image":int,"code":string [A-Z0-9_]
}
ex: payload={
    "name": "NEW_NAME",
    "weight":"154",
    "image": "2",
    "code":"NEW_CODE"
}
```
***Get/Update/Delete medication by code*** `(method=GET,PATCH,PUT,DELETE)`
```
/api/medications/code/<code>
```
```
only for PUT and PATCH
payload={"name":string [a-zA-Z0-9_-], "weight":double,"image":int,"code":string [A-Z0-9_]
}
ex: payload={
    "name": "NEW_NAME",
    "weight":"154",
    "image": "2",
    "code":"NEW_CODE"
}
```