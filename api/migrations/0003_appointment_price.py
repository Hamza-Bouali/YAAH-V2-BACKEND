# Generated by Django 5.1.5 on 2025-02-04 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_appointment_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
