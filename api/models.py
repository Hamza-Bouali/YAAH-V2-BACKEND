import uuid
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date



class Disease(models.Model):
    """Model representing a disease."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Allergy(models.Model):
    """Model representing an allergy."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Allergies"
        ordering = ['name']

class Prescription(models.Model):
    """Model representing a medical prescription."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medication = models.CharField(max_length=255, help_text="Name of the medication", blank=True)
    dosage = models.CharField(max_length=255,blank=True)
    frequency = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.fromisocalendar(2022, 1, 1))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    duration = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")

    def __str__(self):
        return f"{self.medication} ({self.status}) - {self.patient.name}"

    class Meta:
        ordering = ['-created_at']

class Visit(models.Model):
    """Model representing a patient visit."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    hour = models.TimeField()
    reason = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit on {self.date}  - {self.reason}"

    class Meta:
        ordering = ['-date']
        

class Appointment(models.Model):
    """Model representing a scheduled appointment."""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    place=models.CharField(max_length=255, blank=True,choices=[('Virtual','Virtual'),('In-person','In-person')],default='in-person')
    pat = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='appointments')
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def clean(self):
        if self.date < date.today():
            raise ValidationError("Appointment date cannot be in the past")

    def __str__(self):
        return f"Appointment on {self.date} at {self.time} - {self.patient.name}"

    class Meta:
        ordering = ['date', 'time']



from django.contrib.auth.models import AbstractUser
class Doctor(AbstractUser):
    
    def __str__(self):
        return self.username + " "+ self.email
    


class Patient(models.Model):
    """Model representing a patient in the medical system."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=False, blank=False, default=10, editable=False)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)
    dob = models.DateField()
    blood_type = models.CharField(max_length=3, null=True, blank=True)  # e.g., A+, B-, O+
    treatment = models.TextField(blank=True)
    disease= models.ManyToManyField(Disease, related_name='patient', blank=True)
    visit = models.ManyToManyField(Visit, related_name='patient', blank=True)
    allergies = models.ManyToManyField(Allergy, related_name='patient', blank=True, through=None)
    appointment = models.ManyToManyField(Appointment, related_name='patient', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    medication = models.ManyToManyField(Prescription, related_name='patient', blank=True)

    def calculate_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'dob']  