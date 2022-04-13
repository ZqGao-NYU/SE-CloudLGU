import json

from django.http import JsonResponse
from django.shortcuts import render
from .models import TimeSlot
from django.db.models import Q
from datetime import datetime, timedelta
from accounts.models import my_user
from utils import getStartEnd
# Create your views here.

def CreateSlot(request):
    if(request.method == 'POST'):

        StartTime = request.POST.get('otStartTime')
        EndTime = request.POST.get('otEndTime')
        Location = request.POST.get('otLocation')
        profID = request.POST.get('Professor_userID')
        Date = request.POST.get('otDate')


        Date = datetime.strptime(Date, '%Y-%m-%d')
        StartTime = datetime.strptime(StartTime, '%H:%M')
        EndTime = datetime.strptime(EndTime, '%H:%M')


        context = {}
        # Search whether the time slot was taken up
        today_slots = TimeSlot.objects.filter(otDate=Date)
        if today_slots.exists():
            # Empty Day, Every Time is OK
            pass
        else:
            check_slots = today_slots.get(Q(ProfID = profID),
                Q(otStartTime__range=(StartTime, EndTime)) | Q(otEndTime__range=(StartTime, EndTime)) |
                                          Q(otStartTime__lt=StartTime, otEndTime=EndTime))
            if check_slots.exists():
                context['status'] = {}
                context['status']['response'] = "The Time Period from {start} to {end} Has Already Been. Please Try Again!".format(start=StartTime, end=EndTime)
                context['status']['success'] = False
                context['otID'] = -1
                return JsonResponse(context)

        # Create the slot and Return ID
        slot = TimeSlot()
        slot.otDate = Date
        slot.otStartTime = StartTime
        slot.otEndTime = EndTime
        slot.otLocation = Location
        slot.Professor = my_user.objects.get(id=profID)
        # slot.ProfID = profID
        slot.save()

        context['status'] = {}
        context['status']['response'] = "The Time Period from {start} to {end} at {location} is successfully Created".format(start=StartTime,
                                                                                                     end=EndTime, location = Location)
        context['status']['success'] = True
        context['otID'] = slot.id
        return JsonResponse(context)




def UpdateSlot(request):
    otID = request.POST.get('otID')
    slot = TimeSlot.objects.get(id=otID)

    # New Information
    StartTime = request.POST.get('otStartTime')
    EndTime = request.POST.get('otEndTime')
    Location = request.POST.get('otLocation')
    profID = request.POST.get('Professor_userID')
    Date = request.POST.get('otDate')


    today_slots = TimeSlot.objects.filter(otDate=Date)

    context = {}
    context['status'] = {}
    if today_slots.exists():
        # Empty Day, Every Time is OK
        pass
    else:
        check_slots = today_slots.get(Q(ProfID = profID), ~Q(id = otID),
            Q(otStartTime__range=(StartTime, EndTime)) | Q(otEndTime__range=(StartTime, EndTime)) |
            Q(otStartTime__lt=StartTime, otEndTime=EndTime))
        if check_slots.exists():
            context['status'] = {}
            context['status'][
                'response'] = "The Time Period from {start} to {end} Has Already Been. Please Try Again!".format(
                start=StartTime, end=EndTime)
            context['status']['success'] = False
            context['otID'] = -1
            return JsonResponse(context)

    # Update the slot
    slot.otStartTime = StartTime
    slot.otEndTime = EndTime
    slot.otLocation = Location
    slot.otDate = Date
    slot.save()
    context['status']['response'] = "The Time Period from {start} to {end} at {location} is successfully updated.".format(start=StartTime,
                                                                                                 end=EndTime,
                                                                                                 location=Location)
    context['status']['success'] = True
    context['otID'] = slot.id
    return JsonResponse(context)


def DeleteSlot(request):
    slotID = request.POST.get('otID')
    slot = TimeSlot.objects.get(id=slotID)

    StartTime = slot.otStartTime
    EndTime = slot.otEndTime
    Location = slot.otLocation
    Date = slot.otDate


    context = {}
    context['status'] = {}
    try:
        slot.delete()
        context['response'] = "The Time Period from {start} to {end} at {location} is successfully deleted.".format(start=StartTime,
                                                                                                 end=EndTime,
                                                                                                 location=Location)
        context['success'] = True
        return JsonResponse(context)
    except:
        context['success'] = False
        context['response'] = "The Time Period from {start} to {end} at {location} fail to be deleted.".format(start=StartTime,
                                                                                                 end=EndTime,
                                                                                                 location=Location)
        return JsonResponse(context)


def BookSlot(request):
    slotID = request.POST.get('otID')
    StudentID = request.POST.get('StudentID')

    slot = TimeSlot.objects.get(id=slotID)

    context = {}
    if slot:
        slot.booked = True
        slot.booked_by = my_user.objects.get(id=StudentID)
        context['success'] = True
        return JsonResponse(context)
    else:
        context['success'] = False
        context['response'] = "Cannot Find The Student or Cannot Find the Specified Time Slot!"
        return JsonResponse(context)

def Search_By_Prof_Name(request):
    prof_Name = request.POST.get('Professor_Name')
    get_slots = TimeSlot.objects.filter(Q(Professor__username__contains=prof_Name)).distinct()
    profs = [Prof['Professor'] for Prof in get_slots.only('Professor')]
    response = {}
    if len(profs):
        response['success'] = True
        response['list'] = [json.dumps({'profID': prof.id, 'profName':prof.username}) for prof in profs]
        return JsonResponse(response)
    else:
        response['success'] = False
        response['list'] = []
        return JsonResponse(response)






def Search_By_Time(request):
    today = datetime.today().date()
    Sunday, Saturday = getStartEnd(today)
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday))).distinct()
    profs = [Prof['Professor'] for Prof in get_slots.only('Professor')]
    response = {}
    if len(profs):
        response['success'] = True
        response['list'] = [json.dumps({'profID': prof.id, 'profName':prof.username}) for prof in profs]
        return JsonResponse(response)
    else:
        response['success'] = False
        response['list'] = []
        return JsonResponse(response)



def Student_Check(request):
    today = datetime.today().date()
    Sunday, Saturday = getStartEnd(today)
    profID = request.POST.get('Professor_ID')
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(Professor_id = profID), Q(booked=False))
    response = {}
    if len(get_slots):
        response['success'] = True
        response['lists'] = [json.dumps({'otID': slot.id,
                                         'otStarTime': slot.otStartTime,
                                         'otEndTime': slot.otEndTime,
                                         'otLocation': slot.otLocation,
                                         'prof_name': slot.Professor.username}) for slot in get_slots]
        return JsonResponse(response)
    else:
        response['success'] = False
        response['list'] = []
        return JsonResponse(response)




def Professor_Check(request):
    today = datetime.today().date()
    Sunday, Saturday = getStartEnd(today)
    profID = request.POST.get('Professor_ID')
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(Professor_id = profID))
    response = {}
    if len(get_slots):
        response['success'] = True
        response['lists'] = [json.dumps({'otID': slot.id,
                                         'otStarTime': slot.otStartTime,
                                         'otEndTime': slot.otEndTime,
                                         'otLocation': slot.otLocation,
                                         'isbooked': slot.booked,
                                         'booked_by': slot.booked_by}) for slot in get_slots]
        return JsonResponse(response)
    else:
        response['success'] = False
        response['list'] = []
        return JsonResponse(response)