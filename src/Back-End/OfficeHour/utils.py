from datetime import datetime, timedelta


def get_start_end(today):
    weekday = today.isoweekday()
    delta1 = timedelta(days=weekday)
    delta2 = timedelta(days=6 - weekday)
    Sunday = today - delta1
    Saturday = today + delta2
    return Sunday, Saturday


def converter(TimeSlot):
    return {'otID': TimeSlot.id, 'otDate': TimeSlot.otDate, 'otStartTime': TimeSlot.otStartTime, 'otEndTime': TimeSlot.otEndTime,
            'otLocation': TimeSlot.otLocation, 'isBooked': TimeSlot.booked, 'booked_by': TimeSlot.booked_by}