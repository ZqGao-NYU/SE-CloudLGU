from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('student/show', views.Student_Check),
    path('prof/show', views.Professor_Check),
    path('student/searchtime', views.Search_By_Time),
    path('student/searchprof', views.Search_By_Prof_Name),
    path('student/book', views.BookSlot),
    path('prof/delete', views.DeleteSlot),
    path('prof/update', views.UpdateSlot),
    path('prof/create', views.CreateSlot),
]