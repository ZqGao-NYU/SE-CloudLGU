from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('student/show', views.Student_Check),
    path('professor/show', views.Professor_Check),
    path('student/searchtime', views.Search_By_Time),
    path('student/searchprof', views.Search_By_Prof_Name),
    path('student/book', views.BookSlot),
    path('professor/delete', views.DeleteSlot),
    path('professor/update', views.update_slot),
    path('professor/create', views.create_slot),
]