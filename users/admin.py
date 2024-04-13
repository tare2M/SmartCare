from django.contrib import admin
from .models import CustomUser, Doctor, Patient, Appointment

admin.site.register(CustomUser)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
