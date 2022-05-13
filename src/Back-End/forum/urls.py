from django.urls import path
from . import views

# the urls of functions in app 'forum'
urlpatterns = [
    path('post/create', views.Create_new_post),
    path('post/delete', views.Delete_post),
    path('post/update', views.Update_post),
    path('post/show', views.Show_post),
    path('post/showall', views.Show_all_post),
    path('comment/create', views.Create_new_comment),
    path('comment/delete', views.Delete_comment),
    path('comment/update', views.Update_comment),
]
