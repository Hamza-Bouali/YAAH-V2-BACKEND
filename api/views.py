from django.shortcuts import render, HttpResponse
from .models import Patient
from .serializers import PatientSerializer

from rest_framework import viewsets


# Create your views here.


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


def index(request):
    return HttpResponse('Hello World')


