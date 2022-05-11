from django.db import models
from accounts.models import my_user

# Create your models here.

class forumPost(models.Model):
    Title = models.CharField(max_length=255)  # Required
    Content = models.TextField()
    Tag = models.CharField(max_length=255) #Discussion, Help, Recruit, Top前端筛选
    Ctime = models.DateTimeField()
    UpdateTime = models.DateTimeField()
    Poster = models.ForeignKey(my_user, related_name='Poster', on_delete=models.CASCADE)
    class Meta:
        ordering = ['-UpdateTime']


class forumComment(models.Model):
    forumPost = models.ForeignKey(forumPost, on_delete=models.CASCADE, related_name='comments')
    Commenter = models.ForeignKey(my_user, related_name='Commenter', on_delete=models.CASCADE)
    Content = models.TextField()
    Ctime = models.DateTimeField()
    class Meta:
        ordering = ['Ctime']
