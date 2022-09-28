from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url 
from rest_framework import routers
from drones import views

router = routers.DefaultRouter()

router.register(r'api/medications', views.MedicationViewSet)
    
urlpatterns = [
    
    path('', include(router.urls)),    
    url(r'^api/drones/$', views.dronesGetAllView),    
    url(r'^api/drones/delete', views.dronesDeleteAllView),
    url(r'^api/drones/register', views.dronesRegisterView),    
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]