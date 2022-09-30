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
- python manage.py runserver

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
```
/api/drones/register
```
```
payload={}
```
***Get/Update/Delete drone by ID*** `(method=GET,PATCH,PUT,DELETE)`
```
/api/drones/id/<id>
```
```
only for PUT and PATCH
payload={}
```
***Get/Update/Delete drone by Serial Number*** `(method=GET,PATCH,PUT,DELETE)`
```
/api/drones/serial-number/<serial-number>
```
```
only for PUT and PATCH
payload={}
```
***Load drone by ID*** `(method=PATCH)`
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

***Get medications list*** `(method=GET)`
```
/api/medications/ 
```
***Delete all medications*** `(method=DELETE)`
```
/api/medications/delete
```
***Register new medication*** `(method=POST)`
```
/api/medications/register
```
```
payload={}
```