**REQUIREMENTS**
- Python 3.6 ≥ 3.10
- Django 3.2 > 4.0
- Django Rest Framework 3.14.0
- Git > 2.30
- django-cors-headers 3.13.0
- virtualenv package 

**CREATE DIR/INSTALL**
- Install Python 3.6 ≥ 3.10
- Install Git > 2.30
# Create the project directory
# type and run in a console
- mkdir `directory-name`
- cd `directory-name`
- git init
- git remote add origin https://github.com/nestym2f/drones-restapi-mussala-soft.git
- git pull origin master

**BUILD AND RUN**
# Create a virtual environment to isolate packages dependencies for the project
# type and run in a console
- pip install virtualenv
- python3 virtualenv `environment-name`
- source `environment-name`/bin/activate # On Windows use `environment-name`\Scripts\activate
- pip install -r requirements.txt
- cd drones_api
- python manage.py runserver