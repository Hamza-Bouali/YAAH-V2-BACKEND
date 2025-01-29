from rest_framework.serializers import ModelSerializer

from .models import Patient, Visit, Appointment , Allergy, Disease,Prescription


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        Patient = Patient.objects.create(**validated_data)
        Patient.save()
        return Patient
    
    def update(self, instance, validated_data: dict):
        # Update instance fields with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def delete(self, instance):
        instance.delete()
        return instance


class VisitSerializer(ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

    def create(self, validated_data):
        Visit = Visit.objects.create(**validated_data)
        Visit.save()
        return Visit
    
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
        Appointment = Appointment.objects.create(**validated_data)
        Appointment.save()
        return Appointment
    
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
        Allergy = Allergy.objects.create(**validated_data)
        Allergy.save()
        return Allergy
    
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
        Disease = Disease.objects.create(**validated_data)
        Disease.save()
        return Disease
    
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
        Prescription = Prescription.objects.create(**validated_data)
        Prescription.save()
        return Prescription
    
    def update(self, instance, validated_data: dict):
        # Update instance fields with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    def delete(self, instance):
        instance.delete()
        return instance



