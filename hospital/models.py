from django.db import models

# Create your models here.
#hospital model
class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.location}"
#category model

#booking model
class Booking(models.Model):
    name=models.CharField(max_length=255)
    age=models.CharField(max_length=255)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.name} "


