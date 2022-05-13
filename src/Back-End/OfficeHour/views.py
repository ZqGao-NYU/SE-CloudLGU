import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from .models import TimeSlot
from django.db.models import Q, F
from datetime import datetime
from accounts.models import MyUser
from .utils import get_start_end


@require_POST
def create_slot(request):
    """Create The Office Hour at a Certain Time

    Key Arguments:
    start_time: Start time of office hour in HH:MM like 18:00
    end_time: End time of office hour in HH:MM like 19:00
    location: Location to host the office hour
    date: Date of office hour in YYYY-MM-DD like 2022-02-22

    """
    if request.method == 'POST':
        data = json.loads(request.body)
        start_time = data['otStartTime']
        end_time = data['otEndTime']
        location = data['otLocation']
        prof_id = data['Professor_userID']
        date = data['otDate']

        # Clean the data sent from the client
        date = datetime.strptime(date, '%Y-%m-%d')
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')

        context = {}
        # Search whether the time slot was taken up
        today_slots = TimeSlot.objects.filter(otDate=date)
        if not today_slots.exists():
            # Empty Day, Every Time is OK
            pass
        else:
            # Otherwise, check the time conflict with the following ORM
            check_slots = today_slots.filter(Q(Professor_id=prof_id),
                                             Q(otStartTime__gt=start_time, otStartTime__lt=end_time) |
                                             Q(otEndTime__gt=start_time, otEndTime__lt=end_time) |
                                             Q(otStartTime__lt=start_time, otEndTime__gt=end_time))
            if check_slots.exists():
                context['status'] = {}
                context['status'][
                    'response'] = "The Time Period from {start} to {end} Has Already Been Taken Up. Please Try " \
                                  "Another Time!".format(
                    start=start_time, end=end_time)
                context['status']['success'] = False
                context['otID'] = -1
                return JsonResponse(context)
        # Create the slot and Return ID
        slot = TimeSlot()
        slot.otDate = date
        slot.otStartTime = start_time
        slot.otEndTime = end_time
        slot.otLocation = location
        slot.Professor = MyUser.objects.get(id=prof_id)
        slot.save()  # Save the updated entity.

        context['status'] = {}
        context['status'][
            'response'] = "The Time Period from {start} to {end} at {location} is successfully Created".format(
            start=start_time,
            end=end_time, location=location)
        context['status']['success'] = True
        context['otID'] = slot.id
        return JsonResponse(context)

@require_POST
def update_slot(request):
    """ Professor can update their already created time slots"""
    otID = request.POST.get('otID')
    slot = TimeSlot.objects.get(id=otID)
    # New Information
    data = json.loads(request.body)
    StartTime = data['otStartTime']
    EndTime = data['otEndTime']
    Location = data['otLocation']
    Date = data['otDate']
    profID = slot.Professor.id
    today_slots = TimeSlot.objects.filter(Q(otDate=Date), Q(Professor_id=profID))

    context = {'status': {}}
    if not today_slots.exists():
        # Empty Day, Every Time is OK
        pass
    else:
        # Otherwise, check the time conflict with the following ORM
        # Also, note that the updated time can overlap with the old time.
        check_slots = today_slots.filter(~Q(id=otID),
                                         Q(otStartTime__gt=StartTime, otStartTime__lt=EndTime) | Q(
                                             otEndTime__gt=StartTime, otEndTime__lt=EndTime) |
                                         Q(otStartTime__lt=StartTime, otEndTime__gt=EndTime))
        if check_slots.exists():
            context['status'] = {}
            context['status'][
                'response'] = "The Time Period from {start} to {end} Has Already Been Taken Up. Please Try Another " \
                              "Time!".format(
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
    context['status'][
        'response'] = "The Time Period from {start} to {end} at {location} is successfully updated.".format(
        start=StartTime,
        end=EndTime,
        location=Location)
    context['status']['success'] = True
    context['otID'] = slot.id
    return JsonResponse(context)


@require_POST
def delete_slot(request):
    """Professor can delete the time slot too."""
    context = {}
    data = json.loads(request.body)
    slotID = data['otID']
    try:
        slot = TimeSlot.objects.get(id=slotID)  #  Find that slot by id firstly.
    except TimeSlot.DoesNotExist:
        context['success'] = False
        context['response'] = f"Cannot Find The Slot with ID: {slotID}"
        return JsonResponse(context)

    StartTime = slot.otStartTime
    EndTime = slot.otEndTime
    Location = slot.otLocation

    try:
        # Delete the slot and return.
        slot.delete()
        context['response'] = "The Time Period from {start} to {end} at {location} is successfully deleted.".format(
            start=StartTime,
            end=EndTime,
            location=Location)
        context['success'] = True
        return JsonResponse(context)
    except AssertionError:
        context['success'] = False
        context['response'] = "The Time Period from {start} to {end} at {location} fail to be deleted.".format(
            start=StartTime,
            end=EndTime,
            location=Location)
        return JsonResponse(context)


@require_POST
def book_slot(request):
    """Student can book that slot

    Key Arguments:
    slot_id: The slot's id that should be booked.
    student_id: The student's id who books the slot.
    """
    context = {}
    data = json.loads(request.body)
    slot_id = data['otID']
    student_id = data['StudentID']
    try:
        slot = TimeSlot.objects.get(id=slot_id)
    except TimeSlot.DoesNotExist:
        context['response'] = f"Cannot Find The Slot with id:{slot_id}"
        context['success'] = False
        return JsonResponse(context)

    slot.booked = True
    slot.booked_by = MyUser.objects.get(id=student_id)
    slot.save()
    context['success'] = True
    context[
        'response'] = f"You have successfully booked the office time from {slot.otStartTime} to {slot.otEndTime} " \
                      f"at {slot.otLocation} on {slot.otDate} "
    return JsonResponse(context)


@require_POST
def search_by_prof_name(request):
    """Student can get one professor's all time slots in this week by entering his name

    Key Arguments:
    prof_name: Professor's name
    """
    response = {}
    data = json.loads(request.body)
    try:
        prof_name = data["Professor_Name"]
    except:
        response['success'] = False
        return JsonResponse(response)
    # Get the span of this week. We always show the data from last Sunday to this Saturday
    today = datetime.today().date()
    sunday, saturday = get_start_end(today)
    # Filter by prof's name and span of the weekdays.
    get_slots = TimeSlot.objects.filter(Q(Professor__username=prof_name), Q(otDate__range=(sunday, saturday)),
                                        Q(booked=False)).annotate(otID=F("pk")).values("otID", "otStartTime",
                                                                                       "otEndTime", "otDate",
                                                                                       "otLocation")

    if get_slots.exists():
        response['success'] = True
        response['slots'] = list(get_slots)
        return JsonResponse(response)
    else:
        response['success'] = False
        response['list'] = []
        return JsonResponse(response)



@require_GET
def search_by_time(request):
    """Student can get the list of professor's name and """
    response = {}
    today = datetime.today().date()
    Sunday, Saturday = get_start_end(today)
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(booked=False)).annotate(
        profName=F("Professor__username")).values_list('profName',
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



@require_POST
def student_check(request):
    """Student can check the time slots that they booked."""
    today = datetime.today().date()
    Sunday, Saturday = get_start_end(today)
    data = json.loads(request.body)
    studentID = data['Student_ID']
    # Filter the slots that are booked by that student in this week.
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(booked_by=studentID)).annotate(
        otID=F("pk"), prof_name=F("Professor__username")
    ).values("otID", "otDate", "otStartTime", "otEndTime", "otLocation", "prof_name")
    response = {}
    if get_slots.exists():
        response['success'] = True
        response['lists'] = list(get_slots)

        return JsonResponse(response)
    else:
        response['success'] = False
        response['lists'] = []
        return JsonResponse(response)



@require_POST
def professor_check(request):
    """Professor can also check all the time slots he created, and know whether they are booked or not."""
    today = datetime.today().date()
    Sunday, Saturday = get_start_end(today)
    data = json.loads(request.body)
    profID = data['Professor_ID']
    # Filter the slots that created by this professor in this week. Rename the columns by "annotate"
    get_slots = TimeSlot.objects.filter(Q(otDate__range=(Sunday, Saturday)), Q(Professor_id=profID)).annotate(
        otID=F("pk"), isbooked=F("booked"), booked_byName=F("booked_by__username")).values("otID", "otDate",
                                                                                           "otStartTime", "otEndTime",
                                                                                           "otLocation",
                                                                                           "isbooked", "booked_by",
                                                                                           "booked_byName")

    response = {}
    if get_slots.exists():
        response['success'] = True
        response['lists'] = list(get_slots)
        response['Professor_Name'] = MyUser.objects.get(id=profID).username
        return JsonResponse(response)
    else:
        response['success'] = False
        response['list'] = []
        return JsonResponse(response)
