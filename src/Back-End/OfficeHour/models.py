from django.db import models
from accounts.models import my_user
# Create your models here.

class TimeSlot(models.Model):
    otStartTime = models.DateTimeField()
    otEndTime = models.DateTimeField()
    otDate = models.DateTimeField()
    otLocation = models.CharField(max_length=255)
    Professor = models.ForeignKey(my_user, on_delete = models.CASCADE, related_name='hosts')
    # ProfID = models.IntegerField()
    booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(my_user, on_delete = models.CASCADE, related_name='guests', default="")

