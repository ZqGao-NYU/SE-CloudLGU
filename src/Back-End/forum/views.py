from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from .models import forumPost, forumComment
from accounts.models import my_user
from django.core import serializers
import datetime
from django.db.models import F

@require_POST
def Create_new_post(request):
    '''Poster can add a new post to the forum.'''
    # input
    # The front end has already handled illegal input, so no verification is done here

    data = json.loads(request.body)
    postTitle = data['postTitle']
    postContent = data['postContent']
    postTag = data['postTag']
    userID = data['userID']
    # postTitle = request.POST.get('postTitle')
    # postContent = request.POST.get('postContent')
    # postTag = request.POST.get('postTag')
    # userID = request.POST.get('userID')

    # create a new 'forumPost' object
    new_post = forumPost(Title=postTitle, Content=postContent, Tag=postTag)
    poster = my_user.objects.get(id=userID)

    new_post.Poster = poster
    new_post.UpdateTime = datetime.datetime.now()
    new_post.Ctime = datetime.datetime.now()
    new_post.save()

    # return value
    response = {}
    response['postID'] = new_post.id
    response['success'] = True
    return JsonResponse(response)

@require_POST
def Delete_post(request):
    '''The post can be deleted.'''
    # input
    data = json.loads(request.body)
    postID = data['postID']
    # postID = request.POST.get('postID')

    # delete the forumPost object
    forumPost.objects.get(id=postID).delete()

    # return value
    response = {}
    response['success'] = True
    return JsonResponse(response)

@require_POST
def Update_post(request):
    '''The post can be changed.'''
    # input
    data = json.loads(request.body)
    postID = data['postID']
    postTitle = data['postTitle']
    postContent = data['postContent']
    postTag = data['postTag']

    # find the target post and change the data
    my_post = forumPost.objects.get(id=postID)
    my_post.Title = postTitle
    my_post.Content = postContent
    my_post.Tag = postTag
    my_post.UpdateTime = datetime.datetime.now()
    my_post.save()

    # return value
    response = {}
    response['postID'] = my_post.id
    response['success'] = True
    return JsonResponse(response)

@require_POST
def Show_post(request):
    '''
    Show the details of a single post, including the poster, content,
    title, tag, create time and details of all comments of this post.
    '''
    # input
    data = json.loads(request.body)
    postID = data['postID']
    # postID = request.POST.get('postID')

    # find the target post and get all the details needed from the frontend
    my_post = forumPost.objects.get(id=postID)
    comment_list = my_post.comments.annotate(userID=F('Commenter__id'),
                                             commentContent=F('Content'),
                                             createTime=F('Ctime'), commenterName=F('Commenter__username'),
                                             commentID=F('id')).values('commenterName',
                                                                       'userID',
                                                                       'commentContent',
                                                                       'createTime',
                                                                       'commentID')
    json_list = json.dumps(list(comment_list), cls=DjangoJSONEncoder)

    # return value
    response = {}
    response['success'] = True
    response['postTitle'] = my_post.Title
    response['postContent'] = my_post.Content
    response['postTag'] = my_post.Tag
    response['posterName'] = my_post.Poster.username
    response['createTime'] = my_post.Ctime
    response['updateTime'] = my_post.UpdateTime
    response['commentList'] = json.loads(json_list)
    return JsonResponse(response)

@require_POST
def Show_all_post(request):
    '''Show the title, poster, tag and content for all posts.'''
    # no input value needed for this function
    # get details for all posts
    post_list = forumPost.objects.annotate(postID=F('id'), postTitle=F('Title'),
                                           postContent=F('Content'),
                                           postTag=F('Tag'), posterName=F('Poster__username'),
                                           updateTime=F('UpdateTime'), createTime=F('Ctime')).values('postID',
                                                                                                     'postTitle',
                                                                                                     'postContent',
                                                                                                     'postTag',
                                                                                                     'posterName',
                                                                                                     'updateTime',
                                                                                                     'createTime')
    json_list = json.dumps(list(post_list), cls=DjangoJSONEncoder)

    # return value
    response = {}
    response['success'] = True
    response['postList'] = json.loads(json_list)
    return JsonResponse(response)

@require_POST
def Create_new_comment(request):
    '''Commenter can create comment to each post.'''
    # input
    data = json.loads(request.body)
    postID = data['postID']
    userID = data['userID']
    commentContent = data['commentContent']

    # create a new 'forumComment' object
    commenter = my_user.objects.get(id=userID)
    my_post = forumPost.objects.get(id=postID)
    new_commment = forumComment(forumPost=my_post, Content=commentContent)
    new_commment.Commenter = commenter
    new_commment.Ctime = datetime.datetime.now()
    my_post.UpdateTime = datetime.datetime.now()
    my_post.save()
    new_comment.save()

    # return value
    response = {}
    response['commentID'] = new_commment.id
    response['success'] = True
    return JsonResponse(response)

@require_POST
def Delete_comment(request):
    '''The comment can be deleted.'''
    # input
    data = json.loads(request.body)
    commentID = data['commentID']

    # delete forumComment object
    forumComment.objects.get(id=commentID).delete()

    # return value
    response = {}
    response['success'] = True
    return JsonResponse(response)

@require_POST
def Update_comment(request):
    '''The comment can be changed.'''
    # input
    data = json.loads(request.body)
    commentID = data['commentID']
    postID = data['postID']
    commentContent = data['commentContent']

    # find the target comment and change the data
    my_post = forumPost.objects.get(id=postID)
    my_commment = forumComment.objects.get(id=commentID)
    my_commment.Content = commentContent
    my_post.UpdateTime = datetime.datetime.now()
    my_post.save()
    my_commment.save()

    # return value
    response = {}
    response['success'] = True
    return JsonResponse(response)
