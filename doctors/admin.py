from django.contrib import admin
from .models import Doctor, DiseaseSpecializationMapping,DoctorAvailability,Appointment

admin.site.register(Doctor)
admin.site.register(DiseaseSpecializationMapping)
admin.site.register(DoctorAvailability)
admin.site.register(Appointment)

