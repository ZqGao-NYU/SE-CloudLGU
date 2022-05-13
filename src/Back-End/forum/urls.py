from django.urls import path
from . import views

# the urls of functions in app 'forum'
urlpatterns = [
    path('post/create', views.create_new_post),
    path('post/delete', views.delete_post),
    path('post/update', views.update_post),
    path('post/show', views.show_post),
    path('post/showall', views.show_all_post),
    path('comment/create', views.create_new_comment),
    path('comment/delete', views.delete_comment),
    path('comment/update', views.update_comment),
]
