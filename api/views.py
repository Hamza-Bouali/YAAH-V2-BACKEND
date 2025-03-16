from django.shortcuts import render, HttpResponse
from .models import Patient , Visit , Appointment , Allergy , Disease , Prescription , Conversation , Message, Notification, Depense, Revenue
from .serializers import PatientSerializer , VisitSerializer , AppointmentSerializer , AllergySerializer , DiseaseSerializer , PrescriptionSerializer , ConversationSerializer , MessageSerializer, NotificationSerializer,DepenseSerializer,RevenueSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import AllowAny  # Allow access without authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer
# Create your views here.
from rest_framework.renderers import JSONRenderer
import logging
from django.db.models.functions import TruncDate, TruncMonth
from django.db.models import Count, Sum , Case , When , Value , CharField
import uuid

from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger(__name__)




class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        notification_id = response.data.get('id')
        return Response({'notification_id': notification_id}, status=response.status_code)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        notification_id = response.data.get('id')
        return Response({'notification_id': notification_id}, status=response.status_code)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        notification_id = response.data.get('id')
        return Response({'notification_id': notification_id}, status=response.status_code)

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Override default permissions

    @csrf_exempt
    def post(self, request):
        logger.info(f"Login request received: {request.data}")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]  # Override default permissions

    @csrf_exempt
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  # Override default permissions

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

def index(request):
    return HttpResponse('Hello World')

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=True, methods=['get','post','delete','put'])
    def q(self, request):
        conversation_id = request.query_params.get('id', None)
        if conversation_id is not None:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                serializer = self.get_serializer(conversation)
                return Response(serializer.data)
            except Conversation.DoesNotExist:
                return Response({"error": "Conversation not found"}, status=404)
        return Response({"error": "ID parameter is required"}, status=400)

    @action(detail=True, methods=['post'])
    def create_message(self, request, pk=None):
        try:
            conversation = self.get_object()
            data = request.data
            data['conversation'] = conversation.id
            
            # Validate sender field
            sender_id = data.get('sender')
            if not sender_id:
                return Response({"error": "Sender field is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if sender exists
            try:
                sender = get_user_model().objects.get(id=sender_id)
            except get_user_model().DoesNotExist:
                return Response({"error": "Invalid sender ID"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        message_id=response.data.get('id')
        return Response({'message_id': message_id}, status=response.status_code)

"""class AppointmentStatisticsView(APIView):
    permission_classes = [AllowAny]  # Override default permissions
    def get(self, request):
        appointments = Appointment.objects.all()
        total_appointments = appointments.count()
        completed_appointments = appointments.filter(status='completed').count()
        cancelled_appointments = appointments.filter(status='cancelled').count()
        active_appointments = appointments.filter(status='active').count()
        appointments_by_day = appointments.annotate(day=TruncDate('date')).values('day').order_by('day')
        return Response({
            'total_appointments': total_appointments,
            'completed_appointments': completed_appointments,
            'cancelled_appointments': cancelled_appointments,
            'active_appointments': active_appointments,
            'appointments_by_day': appointments_by_day,
        })"""


from time import time
from datetime import date, timedelta


@api_view(['GET'])
def get_statistics(request):
    try:

        patients_count=Patient.objects.all().count()

        today = date.today()
        
        # Get all visits and group by date
        visits = Visit.objects.all()
        last_year_same_day = today.replace(year=today.year - 1)
        this_year_visits = visits.filter(date__range=[last_year_same_day, today])
        visit_stats = visits.annotate(visit_date=TruncDate('date')) \
                           .values('date') \
                           .annotate(count=Count('id')) \
                           .order_by('date')

        # Calculate last week's data 
        # Calculate last week's start (Monday) and end (Sunday)
        today = date.today()
        last_week_monday = today - timedelta(days=today.weekday() + 7)
        last_week_sunday = today - timedelta(days=today.weekday() + 1)
        
        # Get visits for last week
        last_week_visits = visits.filter(date__gte=last_week_monday, date__lte=last_week_sunday)
        last_week_visits_count = last_week_visits.count()
        
        # Get visits by day for last week
        last_week_visits_by_day = last_week_visits.annotate(
            visit_date=TruncDate('date')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        # Calculate this week data
        # Calculate this week's start (Monday) and end (today)

        this_week_monday = today - timedelta(days=today.weekday())
        this_week_sunday = today + timedelta(days=6 - today.weekday())

        # Get visits for this week
        this_week_visits = visits.filter(date__gte=this_week_monday, date__lte=this_week_sunday)
        this_week_visits_count = this_week_visits.count()

        # Get visits by day for this week
        this_week_visits_by_day = this_week_visits.annotate(
            visit_date=TruncDate('date')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        today_appointments = Appointment.objects.filter(date=today).count()
        today_app = AppointmentSerializer(Appointment.objects.filter(date=today), many=True).data

        # revenuce over time:
        revenue_per_month = this_year_visits.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total_revenue=Sum('price')
        ).order_by('month')

        # get patients by age category

        patients_by_age = Patient.objects.annotate(
    age_category=Case(
                When(age__lte=18, then=Value('0-18')),
                When(age__gte=19, age__lte=35, then=Value('19-35')),
                When(age__gte=36, age__lte=50, then=Value('36-50')),
                When(age__gte=51, then=Value('51+')),
                output_field=CharField(),
            )
        ).values('age_category').annotate(
            count=Count('id')
        ).order_by('age_category')


        # Appointemtents stats:

        response = Response({
            'patients_by_age':patients_by_age,
            "patients_count":patients_count,
            'revenue_per_month': revenue_per_month,
            'today_app':today_app,
            "today_appointments":today_appointments,
            "visits": visits.count(),
            
            "visits_per_day": visit_stats,
            "last_week_visits": last_week_visits_count,
            "last_week_visits_by_day": last_week_visits_by_day,
            "this_week_visits": this_week_visits_count,
            "this_week_visits_by_day": this_week_visits_by_day,
        })
        response.acceptmaped_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        
        return response

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['GET'])
def create_user_UUID(request):
    try:
        return Response({"UUID":str(uuid.uuid4())})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    




from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required


from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework_simplejwt.tokens import AccessToken

@api_view(['GET'])
@login_required
def get_user_data(request):
    try:
        user_tooken = request.headers.get('Authorization').split(' ')[1]
        user_id=AccessToken(user_tooken).payload['user_id']
        user = get_user_model().objects.get(id=user_id)
        if user.is_authenticated:
            
                doctor = user
                serializer = DoctorSerializer(doctor)
                return Response(serializer.data)
            
        else:
            return Response({"error": "User is not authenticated"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

from django.http import JsonResponse
from django.conf import settings
import requests

def get_power_bi_token():
    url = f"https://login.microsoftonline.com/{settings.POWER_BI_TENANT_ID}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.POWER_BI_CLIENT_ID,
        "client_secret": settings.POWER_BI_CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
    }
    response = requests.post(url, data=data)
    return response.json()

def get_power_bi_embed_config(request):
    token_data = get_power_bi_token()
    if "access_token" not in token_data:
        return JsonResponse({"error": "Failed to get token"}, status=500)

    embed_url = f"https://app.powerbi.com/dashboardEmbed?dashboardId={settings.POWER_BI_DASHBOARD_ID}"

    return JsonResponse({
        "access_token": token_data["access_token"],
        "embed_url": embed_url
    })



class DepenseViewSet(viewsets.ModelViewSet):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer

    def get_queryset(self):
        user_token = self.request.headers.get('Authorization').split(' ')[1]
        user_id = AccessToken(user_token).payload['user_id']
        user = get_user_model().objects.get(id=user_id)
        return Depense.objects.filter(doctor=user.id)

class RevenueViewSet(viewsets.ModelViewSet):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer

    def get_queryset(self):
        user_token = self.request.headers.get('Authorization').split(' ')[1]
        user_id = AccessToken(user_token).payload['user_id']
        user = get_user_model().objects.get(id=user_id)
        return Revenue.objects.filter(doctor=user.id)