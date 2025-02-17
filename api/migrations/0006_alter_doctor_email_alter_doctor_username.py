# Generated by Django 5.1.5 on 2025-02-05 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_doctor_assurance_number_doctor_city_doctor_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='username',
            field=models.CharField(blank=True, default='Doctor', max_length=50, unique=True),
        ),
    ]
