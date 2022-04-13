from datetime import datetime, timedelta
# def getTime(input):


def getStartEnd(today):
    weekday = today.isoweekday()
    delta1 = timedelta(days=weekday)
    delta2 = timedelta(days=6 - weekday)
    Sunday = today - delta1
    Saturday = today + delta2
    return Sunday, Saturday

