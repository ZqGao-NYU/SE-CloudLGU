from django.db import models
from accounts.models import MyUser


# Create your models here.

class Forumpost(models.Model):
    Title = models.CharField(max_length=255)  # Required
    Content = models.TextField()
    Tag = models.CharField(max_length=255)
    Ctime = models.DateTimeField()
    UpdateTime = models.DateTimeField()
    Poster = models.ForeignKey(MyUser, related_name='Poster', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-UpdateTime']


class Forumcomment(models.Model):
    forumPost = models.ForeignKey(Forumpost, on_delete=models.CASCADE, related_name='comments')
    Commenter = models.ForeignKey(MyUser, related_name='Commenter', on_delete=models.CASCADE)
    Content = models.TextField()
    Ctime = models.DateTimeField()

    class Meta:
        ordering = ['Ctime']
