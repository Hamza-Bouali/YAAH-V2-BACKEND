# your_app/management/commands/generate_medical_data.py

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random
from datetime import timedelta, date
from api.models import Patient, Disease, Allergy, Prescription, Visit, Appointment,Message,Conversation,Doctor,Notification

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
            ("Penicillin", "Allergic reaction to penicillin antibiotics"),
            ("Peanuts", "Severe peanut allergy"),
            ("Latex", "Reaction to latex materials"),
            ("Dairy", "Lactose intolerance and dairy allergy"),
            ("Shellfish", "Allergic reaction to shellfish"),
            ("Pollen", "Seasonal pollen allergy"),
        ]
        return [Allergy.objects.create(name=name, description=desc) for name, desc in allergies_data]

    def create_patients(self, num_patients):
        patients = []
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        for _ in range(num_patients):
            dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
            patient = Patient.objects.create(
                name=fake.name()[:20],  # Ensure the name does not exceed 20 characters
                email=fake.unique.email()[:50],  # Ensure the email does not exceed 50 characters
                phone=fake.phone_number()[:15],  # Ensure the phone number does not exceed 15 characters
                address=fake.address()[:100],  # Ensure the address does not exceed 100 characters
                dob=dob,
                blood_type=random.choice(blood_types),
                sexe=random.choice(['male', 'female']),
                treatment=fake.text(max_nb_chars=200),
            )
            patients.append(patient)
        return patients

    def create_patient_data(self, patients, diseases, allergies):
        for patient in patients:
            # Assign diseases and allergies
            #patient.disease.add(*random.sample(diseases, random.randint(0, len(diseases))))
            #patient.allergies.set([allergy.id for allergy in random.sample(allergies, random.randint(0, len(allergies)))])
            # Create visits
            for _ in range(random.randint(1, 5)):
                visit = Visit.objects.create(
                    hour=fake.time(),
                    date=fake.date_between(start_date='-1y', end_date='today'),
                    reason=random.choice(['Check-up', 'Follow-up', 'Emergency']),
                    price=random.random() * 1000
                )
                patient.visit.add(visit)

            #create diseases 
            for _ in range(random.randint(1, 3)):
                disease=Disease.objects.create(
                    name=fake.word()[:20],
                    description=fake.text(max_nb_chars=200)
                )
                patient.disease.add(disease)

            # Create allergies
            for _ in range(random.randint(1, 3)):
                allergy=Allergy.objects.create(
                    name=fake.word()[:20],
                    description=fake.text(max_nb_chars=200)
                )
                patient.allergies.add(allergy)



            # Create prescriptions with correct fields
            for _ in range(random.randint(1, 3)):
                start_date = fake.date_between(start_date='-1y', end_date='today')
                end_date = start_date + timedelta(days=random.randint(30, 180))
                prescription = Prescription.objects.create(
                    medication=fake.word()[:20],
                    dosage=f"{random.randint(10, 500)}mg",
                    frequency=random.choice(['Daily', 'Twice daily', 'As needed'])[:20],
                    start_date=start_date,
                    end_date=end_date,
                    status=random.choice(['active', 'completed', 'cancelled']),
                    duration=f"{random.randint(1, 6)} months"
                )
                patient.medication.add(prescription)


            # Create appointments
            for _ in range(random.randint(0, 2)):
                hour = random.randint(9, 17)
                appointment_time = f"{hour:02d}:00"
                today = date.today()
                days_offset = int(random.gauss(30, 15))  # Mean of 30 days, std dev of 15 days
                future_date = today + timedelta(days=max(0, min(180, days_offset)))  # Clamp between today and 6 months
                Appointment.objects.create(
                    date=future_date,
                    time=appointment_time,
                    status=random.choice(['scheduled', 'completed', 'cancelled']),
                    pat=patient,
                    place=random.choice(['Virtual', 'In-person']),
                    notes=fake.text(max_nb_chars=200),
                    price=random.random() * 1000
                )

            # Create prescriptions
            for _ in range(random.randint(1, 3)):
                start_date = fake.date_between(start_date='-1y', end_date='today')
                end_date = start_date + timedelta(days=random.randint(30, 180))
                Prescription.objects.create(
                    medication=fake.word()[:20],
                    dosage=f"{random.randint(10, 500)}mg",
                    frequency=random.choice(['Daily', 'Twice daily', 'As needed']),
                    start_date=start_date,
                    end_date=end_date,
                    status=random.choice(['active', 'completed', 'cancelled']),
                    duration=f"{(end_date - start_date).days} days"
                )
            
            # create conversation with patient
            doctor = Doctor.objects.first()
            if not doctor:
                 # Create a default doctor if none exists
                doctor = Doctor.objects.create(username='default_doctor')

            for i in range(10):
                Notification.objects.create(
                    type=random.choice(['message', 'appointment', 'prescription']),
                    title=fake.text(max_nb_chars=10),
                    subtitle=fake.text(max_nb_chars=20),
                    is_seen=random.choice([True, False]),
                    doctor=doctor,
                )


            # Assign doctor to the conversation
            conversation = Conversation.objects.create(doctor=doctor, patient=patient)

            # Assign patient to the conversation
            
            for _ in range(random.randint(1, 5)):
                sent_by = random.choice(['doctor', 'patient'])
                sender = patient
                message = Message.objects.create(
                    sender=sender,
                    sent_by=sent_by,
                    text=fake.text(max_nb_chars=200)
                )
                conversation.messages.add(message)
                print(f"Created message: {message.text}, sent_by: {sent_by}, sender: {sender}")

    
                
