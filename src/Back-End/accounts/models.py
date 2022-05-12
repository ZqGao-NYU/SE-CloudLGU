from django.db import models
from django.contrib.auth.models import User


class MyUser(User):
    """Save User's Basic Information

    Key Arguments:
    identity: User's Identity, Faculty, Student, Administer
    has_confirmed: Whether the user have input the confirmation code.
    """
    identity = models.CharField(max_length=16,
                                choices=(('faculty', 'faculty'), ('student', 'student'), ('admin', 'admin')),
                                default='student')
    has_confirmed = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-c_time"]


class ConfirmString(models.Model):
    """Save MyUser's Confirmation Code and the registered time."""
    code = models.CharField(max_length=256)
    user = models.OneToOneField('MyUser', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-c_time"]  # Order by c_time decreasing order
        verbose_name = "Confirmation_Code"
        verbose_name_plural = "Confirmation_Codes"


class Profile(models.Model):
    """Save self introduction, nickname, and avatar

    Key Arguments
    user: Foreign key to MyUser Table
    userIntro: User's self introduction
    userPhoto: User's avatar
    """
    user = models.OneToOneField('MyUser', on_delete=models.CASCADE)  # Save the foreign key (User's userid)
    userIntro = models.CharField(max_length=400)
    userPhoto = models.ImageField(upload_to='accounts/uploads/', default='accounts/uploads/default.png')
