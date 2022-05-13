from django.contrib import admin
from forum import models
# Register your models here.
admin.site.register(models.Forumpost)
admin.site.register(models.Forumcomment)
