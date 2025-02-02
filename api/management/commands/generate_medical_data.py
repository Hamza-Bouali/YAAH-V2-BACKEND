# your_app/management/commands/generate_medical_data.py

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random
from datetime import timedelta, date
from api.models import Patient, Disease, Allergy, Prescription, Visit, Appointment

fake = Faker()

class Command(BaseCommand):
    help = 'Generates dummy data for the medical system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--patients',
            type=int,
            default=50,
            help='Number of patients to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Patient.objects.all().delete()
            Disease.objects.all().delete()
            Allergy.objects.all().delete()
            Prescription.objects.all().delete()
            Visit.objects.all().delete()
            Appointment.objects.all().delete()

        num_patients = options['patients']

        self.stdout.write('Creating diseases...')
        diseases = self.create_diseases()

        self.stdout.write('Creating allergies...')
        allergies = self.create_allergies()

        self.stdout.write(f'Creating {num_patients} patients...')
        patients = self.create_patients(num_patients)

        self.stdout.write('Creating related data...')
        self.create_patient_data(patients, diseases, allergies)

        self.stdout.write(self.style.SUCCESS('Successfully generated medical data'))

    def create_diseases(self):
        diseases_data = [
            ("Hypertension", "High blood pressure condition"),
            ("Type 2 Diabetes", "Chronic condition affecting blood sugar"),
            ("Asthma", "Respiratory condition"),
            ("Arthritis", "Joint inflammation"),
            ("Migraine", "Severe headaches"),
        ]
        return [Disease.objects.create(name=name, description=desc) for name, desc in diseases_data]

    def create_allergies(self):
        allergies_data = [
            ("Penicillin", "Antibiotic allergy"),
            ("Peanuts", "Food allergy"),
            ("Latex", "Material allergy"),
            ("Dust", "Environmental allergy"),
        ]
        return [Allergy.objects.create(name=name, description=desc) for name, desc in allergies_data]

    def create_patients(self, num_patients):
        patients = []
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        for _ in range(num_patients):
            dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
            patient = Patient.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                address=fake.address(),
                dob=dob,
                blood_type=random.choice(blood_types),
                treatment=fake.text(max_nb_chars=200),
            )
            patients.append(patient)
        return patients

    def create_patient_data(self, patients, diseases, allergies):
        for patient in patients:
            # Assign diseases and allergies
            patient.disease.add(*random.sample(diseases, random.randint(0, min(2, len(diseases)))))
            patient.allergies.add(*random.sample(allergies, random.randint(0, min(2, len(allergies)))))
            # Create visits
            for _ in range(random.randint(1, 5)):
                visit = Visit.objects.create(
                    hour=fake.time(),
                    date=fake.date_between(start_date='-1y', end_date='today'),
                    reason=random.choice(['Check-up', 'Follow-up', 'Emergency'])
                )
                patient.visit.add(visit)


            # Create prescriptions with correct fields
            for _ in range(random.randint(1, 3)):
                start_date = fake.date_between(start_date='-1y', end_date='today')
                end_date = start_date + timedelta(days=random.randint(30, 180))
                prescription = Prescription.objects.create(
                    medication=fake.word(),
                    dosage=f"{random.randint(10, 500)}mg",
                    frequency=random.choice(['Daily', 'Twice daily', 'As needed']),
                    start_date=start_date,
                    end_date=end_date,
                    status=random.choice(['active', 'completed', 'cancelled']),
                    duration=f"{random.randint(1, 6)} months"
                )
                patient.medication.add(prescription)


            # Create appointments
            for _ in range(random.randint(0, 2)):
                appointment = Appointment.objects.create(
                    date=fake.date_between(start_date='today', end_date='+6m'),
                    time=fake.time(),
                    status=random.choice(['scheduled', 'completed', 'cancelled', 'no_show'])
                )
                patient.appointment.add(appointment)

            # Create prescriptions
            for _ in range(random.randint(1, 3)):
                start_date = fake.date_between(start_date='-1y', end_date='today')
                end_date = start_date + timedelta(days=random.randint(30, 180))
                Prescription.objects.create(
                    medication=fake.word(),
                    dosage=f"{random.randint(10, 500)}mg",
                    frequency=random.choice(['Daily', 'Twice daily', 'As needed']),
                    start_date=start_date,
                    end_date=end_date,
                    status=random.choice(['active', 'completed', 'cancelled']),
                    duration=f"{(end_date - start_date).days} days"
                )
