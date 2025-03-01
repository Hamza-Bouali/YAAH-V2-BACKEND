import uuid
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date



class Facture(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date=models.DateField(auto_created=True)
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    source=models.CharField(max_length=255, blank=True)


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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

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
    """Model representing a doctor in the medical system."""

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name=models.CharField(max_length=50, blank=True,default='Doctor',null=True)
    last_name=models.CharField(max_length=50, blank=True,default='Doctor',null=True)
    phone_number=models.CharField(max_length=50, blank=True,default='123456789')
    city=models.CharField(max_length=50, blank=True,default='Morocco')
    dob=models.DateField(blank=True,default=date.today)
    email=models.EmailField(blank=True, null=True)
    username=models.CharField(max_length=50, blank=True,default='Doctor',unique=True)
    def __str__(self):
        return self.username + " "+ self.email
    
    def calculate_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    def __str__(self):
        return self.username + " " + (self.email or '')

    def clean(self):
        if self.dob > date.today():
            raise ValidationError("Date of birth cannot be in the future")
        
    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['username']

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
    sexe=models.CharField(max_length=8, blank=True,choices=[('female','female'),('male','male')],default='male')

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

class Message(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender=models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='messages')
    sent_by=models.CharField(max_length=255, blank=True)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Message from {self.sender.name} in {self.conversation}"

class Conversation(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient=models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='conversations')
    doctor=models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='conversations')
    created_at=models.DateTimeField(auto_now_add=True)
    messages=models.ManyToManyField(Message, related_name='conversation', blank=True)
    def __str__(self):
        return f"Conversation between {self.patient.name} and {self.doctor.username}"
    
    class Meta:
        ordering = ['-created_at']