from django.contrib import admin
from .models import forumPost, forumComment
# Register your models here.

admin.site.register(forumPost)
admin.site.register(forumComment)