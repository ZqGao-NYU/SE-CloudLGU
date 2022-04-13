from django.shortcuts import render
from django.http import Http404, JsonResponse
from postComment.models import forumPost, forumComment
from accounts.models import my_user
import datetime

# Create your views here.
def Create_new_post(request):
    #未检测各类非法输入
    postTitle = request.POST.get('postTitle')
    postContent = request.POST.get('postContent')
    postTag = request.POST.get('postTag')
    userID = request.POST.get('userID')

    new_post = forumPost(Title=postTitle, Content=postContent, Tag=postTag)
    poster = my_user.objects.get(id=userID)
    new_post.Poster = poster.username
    new_post.UpdateTime = datetime.datetime.now()
    new_post.save()

    response = {}
    response['postID'] = new_post.id()
    response['success'] = True
    return JsonResponse(response)

def Delete_post(request):
    postID = request.POST.get('postID')
    forumPost.objects.get(id=postID).delete()
    response = {}
    response['success'] = True
    return JsonResponse(response)

def Update_post(request):
    postID = request.POST.get('postID')
    postTitle = request.POST.get('postTitle')
    postContent = request.POST.get('postContent')
    postTag = request.POST.get('postTag')
    my_post = forumPost.objects.get(id=postID)
    my_post.Title = postTitle
    my_post.Content = postContent
    my_post.Tag = postTag
    my_post.save()


