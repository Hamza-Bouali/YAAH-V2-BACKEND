from rest_framework.serializers import ModelSerializer

from .models import Patient


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
