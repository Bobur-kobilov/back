from datetime                   import datetime, date
from pytz                       import timezone
import pytz
from django.conf                import settings

def removeMsec(time):
    if isinstance(time, str):
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    time = time.strftime("%Y-%m-%d %H:%M:%S")
    return time

def localToUtc(time = None):
    if time is not None:
        local_start = datetime.strptime((time + ' 00:00:00'), "%Y-%m-%d %H:%M:%S")
        time = local_start.astimezone(timezone('UTC')).strftime("%Y-%m-%d %H:%M:%S")
    return time

def utcToLocal(time = None):
    if time is not None:
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
        time = time.astimezone(timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")
    return time

def utc_datetime_to_local(time = None):
    if time is not None:
        if isinstance(time, str):
            time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')

        time = time.replace(tzinfo=pytz.UTC)
        time = time.astimezone(timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")
    return time

def set_time_zone(time, time_zone, type):
    if type == 'start':
        time = datetime.strptime((time + ' 00:00:00'), "%Y-%m-%d %H:%M:%S")
    elif type == 'end':
        time = datetime.strptime((time + ' 23:59:59'), "%Y-%m-%d %H:%M:%S")
    return time.replace(tzinfo=time_zone).strftime("%Y-%m-%d %H:%M:%S")