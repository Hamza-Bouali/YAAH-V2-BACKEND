from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Patient, Visit, Appointment , Allergy, Disease,Prescription
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            else:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Username and password are required')



class VisitSerializer(ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

    def create(self, validated_data):
        visit = Visit.objects.create(**validated_data)
        visit.save()
        return visit
    
    def update(self, instance, validated_data: dict):
        # Update instance fields with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def delete(self, instance):
        instance.delete()
        return instance
    

class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        appointment = Appointment.objects.create(**validated_data)
        appointment.save()
        return appointment
    
    def update(self, instance, validated_data: dict):
        # Update instance fields with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def delete(self, instance):
        instance.delete()
        return instance
    

class AllergySerializer(ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'

    def create(self, validated_data):
        allergy = Allergy.objects.create(**validated_data)
        allergy.save()
        return allergy
    
    def update(self, instance, validated_data: dict):
        # Update instance fields with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def delete(self, instance):
        instance.delete()
        return instance
    

class DiseaseSerializer(ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

    def create(self, validated_data):
        disease = Disease.objects.create(**validated_data)
        disease.save()
        return disease
    
    def update(self, instance, validated_data: dict):
        # Update instance fields with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def delete(self, instance):
        instance.delete()
        return instance
    

class PrescriptionSerializer(ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

    def create(self, validated_data):
        prescription = Prescription.objects.create(**validated_data)
        prescription.save()
        return prescription
    
    def update(self, instance, validated_data: dict):
        # Update instance fields with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def delete(self, instance):
        instance.delete()
        return instance




class PatientSerializer(ModelSerializer):
    diseases = DiseaseSerializer(many=True, read_only=True)
    allergies = AllergySerializer(many=True, read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    visits = VisitSerializer(many=True, read_only=True)
    appointments = AppointmentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


