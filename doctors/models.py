from django.db import models
from django.contrib.auth import get_user_model
from hospital.models import Hospital,Booking


User=get_user_model()


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE,null=True)
    # Add more fields like availability, location, etc., if needed

    def __str__(self):
        return f"{self.name} ({self.specialization})"


class DiseaseSpecializationMapping(models.Model):
    disease_name = models.CharField(max_length=100, unique=True)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.disease_name} → {self.specialization}"
class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'date', 'time_slot')

    def __str__(self):
        return f"{self.doctor.name} - {self.date} {self.time_slot}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    date = models.DateField()
    time_slot = models.TimeField()
    age = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    predicted_disease = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')

    def __str__(self):
        return f"{self.user.username} - {self.doctor.name} on {self.date} at {self.time_slot} ({self.status})"

