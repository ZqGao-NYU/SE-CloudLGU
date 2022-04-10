from django.shortcuts import render
from .models import TimeSlot
from datetime import datetime
# Create your views here.

def CreateSlot(request):
    if(request.method == 'POST'):
        StartTime = request.POST.get('otStartTime')
        EndTime = request.POST.get('otEndTime')
        Location = request.POST.get('otLocation')
        profID = request.POST.get('Professor_userID')
        Date = request.POST.get('otDate')
    Date = datetime.strptime('%Y-%m-%d')
    StartTime = datetime.strptime('%H:%M')
    EndTime = datetime.strptime('%H:%M')
    times = TimeSlot.objects.filter(otDate=)



