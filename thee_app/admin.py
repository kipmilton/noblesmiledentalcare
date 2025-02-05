from django.contrib import admin

# Register your models here.
from .models import  Appointment



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date', 'department', 'doctor', 'message')