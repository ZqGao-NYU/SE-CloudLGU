import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from .models import TimeSlot
from django.db.models import Q, F
from datetime import datetime, timedelta
from accounts.models import my_user
from .utils import getStartEnd, converter
from itertools import groupby
import pandas as pd
# Create your views here.

def CreateSlot(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        StartTime = data['otStartTime']
        EndTime = data['otEndTime']
        Location = data['otLocation']
        profID = data['Professor_userID']
        Date = data['otDate']


        Date = datetime.strptime(Date, '%Y-%m-%d')
        StartTime = datetime.strptime(StartTime, '%H:%M')
        EndTime = datetime.strptime(EndTime, '%H:%M')


        context = {}
        # Search whether the time slot was taken up
        today_slots = TimeSlot.objects.filter(otDate=Date)
        if not today_slots.exists():
            # Empty Day, Every Time is OK
            pass
        else:
            check_slots = today_slots.filter(Q(Professor_id = profID),
                                             Q(otStartTime__gt=StartTime, otStartTime__lt = EndTime) |
                                             Q(otEndTime__gt=StartTime, otEndTime__lt = EndTime) |
                                             Q(otStartTime__lt=StartTime, otEndTime__gt =EndTime))
            if check_slots.exists():
                context['status'] = {}
                context['status']['response'] = "The Time Period from {start} to {end} Has Already Been Taken Up. Please Try Another Time!".format(start=StartTime, end=EndTime)
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
    data = json.loads(request.body)
    StartTime =data['otStartTime']
    EndTime = data['otEndTime']
    Location = data['otLocation']
    Date = data['otDate']

    profID = slot.Professor.id
    today_slots = TimeSlot.objects.filter(Q(otDate=Date), Q(Professor_id=profID))

    context = {}
    context['status'] = {}
    if not today_slots.exists():
        # Empty Day, Every Time is OK
        pass
    else:
        check_slots = today_slots.filter(~Q(id = otID),
            Q(otStartTime__gt=StartTime, otStartTime__lt = EndTime) | Q(otEndTime__gt=StartTime, otEndTime__lt = EndTime) |
            Q(otStartTime__lt=StartTime, otEndTime__gt =EndTime))
        if check_slots.exists():
            context['status'] = {}
            context['status'][
                'response'] = "The Time Period from {start} to {end} Has Already Been Taken Up. Please Try Another Time!".format(
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
    context = {}
    data = json.loads(request.body)
    slotID = data['otID']
    try:
        slot = TimeSlot.objects.get(id=slotID)
    except TimeSlot.DoesNotExist:
        context['success'] = False
        context['response'] = f"Cannot Find The Slot with ID: {slotID}"
        return JsonResponse(context)

    StartTime = slot.otStartTime
    EndTime = slot.otEndTime
    Location = slot.otLocation
    Date = slot.otDate


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
    context = {}
    data = json.loads(request.body)
    slotID = data['otID']
    StudentID = data['StudentID']
    try:
        slot = TimeSlot.objects.get(id=slotID)
    except TimeSlot.DoesNotExist:
        context['response'] = f"Cannot Find The Slot with id:{slotID}"
        context['success'] = False
        return JsonResponse(context)

    slot.booked = True
    slot.booked_by = my_user.objects.get(id=StudentID)
    slot.save()
    context['success'] = True
    context['response'] = f"You have successfully booked the office time from {slot.otStartTime} to {slot.otEndTime} at {slot.otLocation} on {slot.otDate}"
    return JsonResponse(context)

def Search_By_Prof_Name(request):
    response = {}
    if(request.method=="GET"):
        response['success'] = False
        return JsonResponse(response)
    data = json.loads(request.body)
    try:
        prof_Name = data["Professor_Name"]
    except:
        response['success'] = False
        return JsonResponse(response)
    today = datetime.today().date()
    Sunday, Saturday = getStartEnd(today)
    get_slots = TimeSlot.objects.filter(Q(Professor__username=prof_Name), Q(otDate__range=(Sunday, Saturday)), Q(booked=False)).annotate(otID=F("pk")).values("otID","otStartTime", "otEndTime", "otDate",
                                                                                        "otLocation")

    if get_slots.exists():
        response['success'] = True
        # response['slots'] = json.loads(serializers.serialize("json", get_slots, fields=("otStartTime", "otEndTime", "otDate",
        #                                                                                 "otLocation", "Professor", "booked", "booked_by")))
        response['slots'] = list(get_slots)
        return JsonResponse(response)
    else:
        response['success'] = False
        response['list'] = []
        return JsonResponse(response)


def Search_By_Time(request):
    response = {}
    today = datetime.today().date()
    Sunday, Saturday = getStartEnd(today)
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(booked = False)).annotate(profName=F("Professor__username")).values_list('profName',
                                                                                                            'otDate').distinct()
    if get_slots.exists():
        response['success'] = True
        result = {}
        for data in get_slots.values('profName', 'otDate'):
            if data['profName'] in result:
                result[data['profName']].append(data['otDate'])
            else:
                result[data['profName']] = []
                result[data['profName']].append(data['otDate'])
        response['lists'] = result
        return JsonResponse(response)

    else:
        response['success'] = False
        response['otLists'] = []
        return JsonResponse(response)



def Student_Check(request):
    today = datetime.today().date()
    Sunday, Saturday = getStartEnd(today)
    data = json.loads(request.body)
    studentID =data['Student_ID']
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(booked_by=studentID)).annotate(otID=F("pk"), prof_name = F("Professor__username")
                                                                                                              ).values("otID", "otDate", "otStartTime","otEndTime","otLocation","prof_name")
    response = {}
    if get_slots.exists():
        response['success'] = True
        response['lists'] = list(get_slots)

        return JsonResponse(response)
    else:
        response['success'] = False
        response['lists'] = []
        return JsonResponse(response)




def Professor_Check(request):
    today = datetime.today().date()
    Sunday, Saturday = getStartEnd(today)
    data = json.loads(request.body)
    profID = data['Professor_ID']
    # get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(Professor_id=profID)).annotate(otID=F("pk"), isbooked=F("booked"),
    #                                                                                                           Professor_Name=F("Professor__username")).values("Professor_Name", "otID", "otDate",
    #                                                                                                                                "otStartTime","otEndTime",
    #                                                                                                                                "otLocation",
    #                                                                                                                                "isbooked","booked_by")
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(Professor_id=profID)).annotate(otID=F("pk"), isbooked=F("booked"), booked_byName=F("booked_by__username")).values("otID", "otDate",
                                                                                                                                   "otStartTime","otEndTime",
                                                                                                                                   "otLocation",
                                                                                                                                   "isbooked","booked_by", "booked_byName")
    # get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(Professor_id=profID)).annotate(otID=F("pk"), isbooked=F("booked")).values("otID", "otDate",
    #                                                                                                                                "otStartTime","otEndTime",
    #                                                                                                                                "otLocation",
    #                                                                                                                                "isbooked","booked_by")

    response = {}
    if get_slots.exists():
        response['success'] = True
        response['lists'] = list(get_slots)
        response['Professor_Name'] = my_user.objects.get(id=profID).username
        return JsonResponse(response)
    else:
        response['success'] = False
        response['list'] = []
        return JsonResponse(response)