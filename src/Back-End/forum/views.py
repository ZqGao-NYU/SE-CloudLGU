from django.shortcuts import render
import json
from django.http import Http404, JsonResponse
from forum.models import forumPost, forumComment
from accounts.models import my_user
from django.core import serializers
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

    response = {}
    response['postID'] = my_post.id()
    response['success'] = True
    return JsonResponse(response)

def Show_post(request):
    postID = request.POST.get('postID')
    my_post = forumPost.objects.get(id=postID)
    comment_list = my_post.comments.all()
    json_list = serializers.serialize("json", comment_list)

    response = {}
    response['success'] = True
    response['postTitle'] = my_post.Title
    response['postContent'] = my_post.Content
    response['postTag'] = my_post.Tag
    response['posterName'] = my_post.Poster
    response['createTime'] = my_post.Ctime
    response['updateTime'] = my_post.UpdateTime
    response['commentList'] = json_list
    return JsonResponse(response)

def Show_all_post(request):
    post_list = forumPost.objects.all()
    json_list = serializers.serialize("json", post_list)

    response = {}
    response['success'] = True
    response['postList'] = json_list
    return JsonResponse(response)

def Create_new_comment(request):
    postID = request.POST.get('postID')
    userID = request.POST.get('userID')
    commentContent = request.POST.get('commentContent')
    my_post = forumPost.objects.get(id=postID)
    commenter = my_user.objects.get(id=userID)
    new_commment = forumComment(forumPost=my_post, Content=commentContent)
    new_commment.Commenter = commenter.username
    new_commment.save()

    response = {}
    response['commentID'] = new_commment.id
    response['success'] = True
    return JsonResponse(response)

def Delete_comment(request):
    commentID = request.POST.get('commentID')
    forumComment.objects.get(id=commentID).delete()
    response = {}
    response['success'] = True
    return JsonResponse(response)

def Update_comment(request):
    commentID = request.POST.get('commentID')
    postID = request.POST.get('postID')
    commentContent = request.POST.get('commentContent')
    my_post = forumPost.objects.get(id=postID)
    my_commment = forumComment.objects.get(id=commentID)
    my_commment.Content = commentContent
    my_commment.save()
    response = {}
    response['success'] = True
    return JsonResponse(response)
