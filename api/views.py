from django.shortcuts import render, HttpResponse
from .models import Patient , Visit , Appointment , Allergy , Disease , Prescription 
from .serializers import PatientSerializer , VisitSerializer , AppointmentSerializer , AllergySerializer , DiseaseSerializer , PrescriptionSerializer
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny  # Allow access without authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer
# Create your views here.
from rest_framework.renderers import JSONRenderer
import logging
from django.db.models.functions import TruncDate
from django.db.models import Count

logger = logging.getLogger(__name__)

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Override default permissions
    def post(self, request):
        logger.info(f"Login request received: {request.data}")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]  # Override default permissions
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
        today = date.today()
        
        # Get all visits and group by date
        visits = Visit.objects.all()
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



        response = Response({
            "visits": visits.count(),
            "visits_per_day": visit_stats,
            "last_week_visits": last_week_visits_count,
            "last_week_visits_by_day": last_week_visits_by_day,
            "this_week_visits": this_week_visits_count,
            "this_week_visits_by_day": this_week_visits_by_day,
        })
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        
        return response

    except Exception as e:
        return Response({"error": str(e)}, status=500)