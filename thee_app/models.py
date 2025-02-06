from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    date = models.DateTimeField()
    department = models.CharField(max_length=100, default="General")
    doctor = models.CharField(max_length=100, default="General")
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('done', 'Done')],
        default='pending'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    proof_of_payment = models.ImageField(upload_to="proofs/", blank=True, null=True)

    def __str__(self):
        return f"Appointment for {self.name} with {self.doctor} on {self.date}"



# accounts/models.py

class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # You may want to hash this later
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
