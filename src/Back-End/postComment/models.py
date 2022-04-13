from django.db import models
from accounts.models import my_user


# Create your models here.

class forumPost(models.Model):
    Title = models.CharField(blank=False, null=False)  # Required
    Content = models.TextField()
    Tag = models.CharField()
    Poster = models.CharField()
    Ctime = models.DateTimeField(auto_now_add=True)
    UpdateTime = models.TimeField()
    # Poster = models.ForeignKey(my_user)
    class Meta:
        ording = ['-Tag', '-UpdateTime']#先tag降序，然后更新时间降序排列


class forumComment(models.Model):
    forumPost = models.ForeignKey(forumPost, on_delete=models.CASCADE)
    Commenter = models.CharField()
    # Commenter = models.Foreignkey(my_user. on_delete=models.CASCADE)
    Content = models.TextField()
    Ctime = models.DateTimeField(auto_now_add=True)#save后重写post的updatetime forum.forumPost.UpdateTime=forum.Ctime
