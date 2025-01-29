from django.contrib import admin
from django.urls import path, include
from .views import index
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, VisitViewSet, AppointmentViewSet, AllergyViewSet, DiseaseViewSet, PrescriptionViewSet



router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='Patients')
router.register(r'visits', VisitViewSet, basename='Visits')
router.register(r'appointments', AppointmentViewSet, basename='Appointments')
router.register(r'allergies', AllergyViewSet, basename='Allergies')
router.register(r'diseases', DiseaseViewSet, basename='Diseases')
router.register(r'prescriptions', PrescriptionViewSet, basename='Prescriptions')



urlpatterns = [
    path('index/',view=index,name='index'),
    *router.urls,
]