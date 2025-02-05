from django.contrib import admin
from django.urls import path, include
from .views import index,create_user_UUID
from rest_framework.routers import DefaultRouter
from .views import get_statistics,PatientViewSet, VisitViewSet, AppointmentViewSet, AllergyViewSet, DiseaseViewSet, PrescriptionViewSet,UserRegistrationView, UserLoginView,ConversationViewSet,MessageViewSet,get_user_data


router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='Patients')
router.register(r'visits', VisitViewSet, basename='Visits')
router.register(r'appointments', AppointmentViewSet, basename='Appointments')
router.register(r'allergies', AllergyViewSet, basename='Allergies')
router.register(r'diseases', DiseaseViewSet, basename='Diseases')
router.register(r'prescriptions', PrescriptionViewSet, basename='Prescriptions')
router.register(r'conversations', ConversationViewSet, basename='Conversations')
router.register(r'messages', MessageViewSet, basename='Messages')




urlpatterns = [
    path('index/',view=index,name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),  
    path('statistics/', view=get_statistics, name='statistics'),
    path('user_id/', view=create_user_UUID, name='create_user_UUID'),
    path('get_user_data/', view=get_user_data, name='get_user_data'),
    
    *router.urls,
]