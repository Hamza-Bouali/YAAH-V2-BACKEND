from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(Disease)
admin.site.register(Allergy)
admin.site.register(Appointment)
admin.site.register(Visit)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Doctor)