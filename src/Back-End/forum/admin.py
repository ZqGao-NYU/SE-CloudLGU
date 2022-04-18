from django.contrib import admin
from forum import models
# Register your models here.
admin.site.register(models.forumPost)
admin.site.register(models.forumComment)
