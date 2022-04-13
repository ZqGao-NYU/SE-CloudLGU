from datetime import datetime, timedelta

from django.test import TestCase

# Create your tests here.
def getStartEnd(today):
    weekday = today.isoweekday()
    delta1 = timedelta(days=weekday)
    delta2 = timedelta(days=6 - weekday)
    Sunday = today - delta1
    Saturday = today + delta2
    return Sunday, Saturday



c1, c2 = getStartEnd(datetime.today().date())

print(c1, c2)
print(datetime.today().date())