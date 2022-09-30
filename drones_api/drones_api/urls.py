from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url 
from rest_framework import routers
from drones import views

router = routers.DefaultRouter()
    
urlpatterns = [   
    url(r'^api/drones/$', views.dronesGetAllView),    
    url(r'^api/drones/delete', views.dronesDeleteAllView),
    url(r'^api/drones/register', views.dronesRegisterView),  
    url(r'^api/drones/id/(?P<pk>[0-9]+)', views.droneDetailView),
    url(r'^api/drones/serial-number/(?P<serialNumber>\w+)', views.droneDetailView),
    url(r'^api/drones/load-medications/id/(?P<pk>[0-9]+)', views.droneLoadMedicationsView),
    url(r'^api/drones/load-medications/serial-number/(?P<serialNumber>\w+)', views.droneLoadMedicationsView),
    url(r'^api/drones/check-loaded-medications/id/(?P<pk>[0-9]+)', views.checkingLoadedDroneView),
    url(r'^api/drones/check-loaded-medications/serial-number/(?P<serialNumber>\w+)', views.checkingLoadedDroneView),
    
    url(r'^api/medications/$', views.medicationGetAllView),
    url(r'^api/medications/delete', views.medicationDeleteAllView),
    url(r'^api/medications/register', views.medicationRegisterView),
    
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]