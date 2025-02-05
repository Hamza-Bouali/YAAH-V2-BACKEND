from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Patient, Visit, Appointment , Allergy, Disease,Prescription, Conversation, Message
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    first_name=serializers.CharField(write_only=True)
    last_name=serializers.CharField(write_only=True)
    email=serializers.EmailField(write_only=True)
    phone_number=serializers.CharField(write_only=True)
    city=serializers.CharField(write_only=True)
    dob=serializers.DateField(write_only=True,input_formats=['%d/%m/%Y'])
    assurance_number=serializers.CharField(write_only=True)
    inassurance=serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'city', 'dob', 'assurance_number', 'inassurance']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            city=validated_data['city'],
            dob=validated_data['dob'],
            assurance_number=validated_data['assurance_number'],
            inassurance=validated_data['inassurance'],
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
                access_token = AccessToken.for_user(user)  # Only generate access token
                return {
                    'access': str(access_token),  # Return only the access token
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
    diseases = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    allergies = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Allergy.objects.all(), 
        read_only=False
    )
    prescriptions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    visits = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    appointments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'

    def update(self, instance, validated_data):
        # Handle Many-to-Many fields properly
        instance.age=instance.calculate_age()
        if 'allergies' in validated_data:
            instance.allergies.set(validated_data.pop('allergies'))
        if 'diseases' in validated_data:
            instance.diseases.set(validated_data.pop('diseases'))
        if 'prescriptions' in validated_data:
            instance.prescriptions.set(validated_data.pop('prescriptions'))
        if 'visits' in validated_data:
            instance.visits.set(validated_data.pop('visits'))
        if 'appointments' in validated_data:
            instance.appointments.set(validated_data.pop('appointments'))

        return super().update(instance, validated_data)




class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        message.save()
        return message
    
    def update(self, instance, validated_data: dict):
        # Update instance fields with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def delete(self, instance):
        instance.delete()
        return instance
    

class ConversationSerializer(ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

    def create(self, validated_data):
        conversation = Conversation.objects.create(**validated_data)
        conversation.save()
        return conversation
    
    def update(self, instance, validated_data: dict):
        # Update instance fields with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def delete(self, instance):
        instance.delete()
        return instance
    
