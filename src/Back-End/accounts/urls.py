from django.urls import path
from . import views

urlpatterns = [
    path('resetProfile', views.resetProfile),
    path('getList', views.getUserList),
]