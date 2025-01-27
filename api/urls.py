from django.contrib import admin
from django.urls import path, include
from .views import index
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet



router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='Patients')


urlpatterns = [
    path('index/',view=index,name='index'),
    *router.urls,
]