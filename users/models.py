from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    age=models.CharField(max_length=3, blank=True,null=True)
    hereditary_diseases = models.CharField(max_length=255, blank=True, default='None')
    other_medical_details = models.CharField(max_length=255, blank=True, default='None')
    blood_group = models.CharField(max_length=10, blank=True,null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username
