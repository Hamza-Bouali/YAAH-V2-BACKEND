from django.contrib import admin
from django.urls import path, include
from .views import index
from rest_framework.routers import DefaultRouter
from .views import get_statistics,PatientViewSet, VisitViewSet, AppointmentViewSet, AllergyViewSet, DiseaseViewSet, PrescriptionViewSet,UserRegistrationView, UserLoginView
from rest_framework_simplejwt.views import TokenObtainPairView,token_refresh


router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='Patients')
router.register(r'visits', VisitViewSet, basename='Visits')
router.register(r'appointments', AppointmentViewSet, basename='Appointments')
router.register(r'allergies', AllergyViewSet, basename='Allergies')
router.register(r'diseases', DiseaseViewSet, basename='Diseases')
router.register(r'prescriptions', PrescriptionViewSet, basename='Prescriptions')



urlpatterns = [
    path('index/',view=index,name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokken/refresh/', token_refresh, name='token_refresh'),
    path('statistics/', view=get_statistics, name='statistics'),
    *router.urls,
]