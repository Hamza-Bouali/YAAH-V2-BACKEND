import uuid
from django.db import models





class Prescription(models.Model):
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medication} ({self.status})"


class RecentVisit(models.Model):
    date = models.DateField()
    reason = models.TextField()
    doctor = models.CharField(max_length=255)

    def __str__(self):
        return f"Visit on {self.date} by {self.doctor}"


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Automatically generate UUID
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    treatment = models.TextField()
    diseases = models.JSONField()  # Stores a list of strings
    phone = models.CharField(max_length=20)
    address = models.TextField()
    last_visit = models.DateField()
    dob = models.DateField()
    blood_type = models.CharField(max_length=3)  # e.g., A+, B-, O+
    next_appointment = models.DateField(null=True, blank=True)
    medications = models.JSONField()  # Stores a list of medication names
    allergies = models.JSONField()  # Stores a list of allergy names
    prescriptions = models.ManyToManyField(Prescription, related_name="patients")
    recent_visits = models.ManyToManyField(RecentVisit, related_name="patients")
    next_visit=models.ForeignKey(to='Appointement',on_delete=models.CASCADE,null=True,blank=True,related_name='next_visit_for') 
    

    def get_last_visit(self):
        return self.recent_visits.order_by('-date').first()

    def __str__(self):
        return self.name


class Appointement(models.Model):
    date = models.DateField()
    time = models.TimeField()
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Appointement on {self.date} by {self.doctor}"
