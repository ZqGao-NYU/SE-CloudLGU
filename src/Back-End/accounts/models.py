from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class User(models.Model):
    userID = models.CharField(max_length= 32, unique=True)
    userName = models.CharField(max_length= 32, unique=True)
    userEmail = models.EmailField(blank=True, unique=True)
    identity = models.CharField(max_length=16, choices=(('staff', 'staff'), ('student', 'student')), default='Student')
    has_confirmed = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-c_time"]

# Save User's Confirmation Code and the registered time.
class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "Confirmation_Code"
        verbose_name_plural = "Confirmation_Codes"