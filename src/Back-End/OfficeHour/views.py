import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from .models import TimeSlot
from django.db.models import Q
from datetime import datetime, timedelta
from accounts.models import my_user
from .utils import getStartEnd, converter
from itertools import groupby
import pandas as pd
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
        if not today_slots.exists():
            # Empty Day, Every Time is OK
            pass
        else:
            check_slots = today_slots.filter(Q(Professor_id = profID),
                                             Q(otStartTime__range=(StartTime, EndTime)) |
                                             Q(otEndTime__range=(StartTime, EndTime)) |
                                             Q(otStartTime__lt=StartTime, otEndTime=EndTime))
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
    StartTime = request.POST.get('otStartTime')
    EndTime = request.POST.get('otEndTime')
    Location = request.POST.get('otLocation')
    Date = request.POST.get('otDate')

    profID = slot.Professor.id
    today_slots = TimeSlot.objects.filter(Q(otDate=Date), Q(Professor_id=profID))

    context = {}
    context['status'] = {}
    if not today_slots.exists():
        # Empty Day, Every Time is OK
        pass
    else:
        check_slots = today_slots.filter(~Q(id = otID),
            Q(otStartTime__range=(StartTime, EndTime)) | Q(otEndTime__range=(StartTime, EndTime)) |
            Q(otStartTime__lt=StartTime, otEndTime=EndTime))
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
    slotID = request.POST.get('otID')
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
    slotID = request.POST.get('otID')
    StudentID = request.POST.get('StudentID')
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
    prof_Name = request.POST.get('Professor_Name')
    today = datetime.today().date()
    Sunday, Saturday = getStartEnd(today)
    get_slots = TimeSlot.objects.filter(Q(Professor__username=prof_Name), Q(otDate__range=(Sunday, Saturday)), Q(booked=False)).values("otStartTime", "otEndTime", "otDate",
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
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(booked = False)).values('Professor__username',
                                                                                                            'otDate').distinct()
    if get_slots.exists():
        response['success'] = True

        response['slots'] = list(get_slots)
        return JsonResponse(response)

    response = {}
    if len(otLists):
        response['success'] = True
        response['otLists'] = otLists
        return JsonResponse(response)
    else:
        response['success'] = False
        response['otLists'] = []
        return JsonResponse(response)



def Student_Check(request):
    today = datetime.today().date()
    Sunday, Saturday = getStartEnd(today)
    profID = request.POST.get('Professor_ID')
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(Professor_id = profID), Q(booked=False))
    response = {}
    if len(get_slots):
        response['success'] = True
        response['otLists'] = [json.dumps({'otID': slot.id,
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
        response['Professor_Name'] = my_user.objects.get(id=profID).username
        return JsonResponse(response)
    else:
        response['success'] = False
        response['list'] = []
        response['Professor_Name'] = ""
        return JsonResponse(response)