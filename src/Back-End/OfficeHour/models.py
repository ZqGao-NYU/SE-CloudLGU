from django.db import models
from accounts.models import MyUser


# Create your models here.

class TimeSlot(models.Model):
    otStartTime = models.TimeField()
    otEndTime = models.TimeField()
    otDate = models.DateField()
    otLocation = models.CharField(max_length=255)
    Professor = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='hosts')
    booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='guests', default=None, blank=True,
                                  null=True)
