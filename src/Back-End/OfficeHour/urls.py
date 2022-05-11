from django.urls import path
from . import views

urlpatterns = [
    path('student/show', views.student_check),
    path('professor/show', views.professor_check),
    path('student/searchtime', views.search_by_time),
    path('student/searchprof', views.search_by_prof_name),
    path('student/book', views.book_slot),
    path('professor/delete', views.delete_slot),
    path('professor/update', views.update_slot),
    path('professor/create', views.create_slot),
]