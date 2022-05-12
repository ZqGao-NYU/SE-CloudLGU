from datetime import timedelta


def get_start_end(today):
    """This function read the date of today and return the date of the last Sunday and the next Saturday"""
    weekday = today.isoweekday()
    delta1 = timedelta(days=weekday)
    delta2 = timedelta(days=6 - weekday)
    Sunday = today - delta1
    Saturday = today + delta2
    return Sunday, Saturday


