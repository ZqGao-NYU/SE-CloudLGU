from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class my_user(User):
    identity = models.CharField(max_length=16, choices=(('staff', 'staff'), ('student', 'student')), default='student')
    has_confirmed = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)
    Profile = models.OneToOneField('Profile', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-c_time"]


# Save my_user's Confirmation Code and the registered time.
class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('my_user', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "Confirmation_Code"
        verbose_name_plural = "Confirmation_Codes"

class Profile(models.Model):
    userIntro = models.CharField(max_length=400)
    userPhoto = models.ImageField(upload_to='uploads/')


