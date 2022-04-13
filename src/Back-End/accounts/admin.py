from django.contrib import admin
from accounts import models
# Register your models here.
admin.site.register(models.my_user)
admin.site.register(models.ConfirmString)
