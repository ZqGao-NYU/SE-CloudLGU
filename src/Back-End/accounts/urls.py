from django.urls import path
from . import views

urlpatterns = [
    path('resetProfile', views.reset_profile),
    path('getList', views.get_user_list),
    path('deleteUser', views.delete_user),

]