#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import requests
import datetime
import time
import pytz

def utc_to_local(utc_dt):
    """
        Возвращает дату и время по Москве
    """
    local_tz = pytz.timezone('Europe/Moscow')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary

def get_time_range():
    """
        Возвращает диапазон даты/времени в UNIX-формате от текущего момента плюс 10 дней 
    """
    dt1 = datetime.datetime.utcnow()
    dt2 = dt1 + datetime.timedelta(days=10)
    return time.mktime(dt1.timetuple()), time.mktime(dt2.timetuple())

def parse_event(event):
    """
        Возвращает информацию о ctf-событии
    """
    start_dt = utc_to_local(datetime.datetime.strptime(event['start'].strip()[:-6], '%Y-%m-%dT%H:%M:%S'))
    finish_dt = utc_to_local(datetime.datetime.strptime(event['finish'].strip()[:-6], '%Y-%m-%dT%H:%M:%S'))
    
    result = 'Format: %s\n' % event['format'].strip()
    result += 'Title: %s\n' % event['title'].strip()
    result += 'Start: %s\n' % start_dt.strftime('%b %d %H:%M:%S')
    result += 'Finish: %s\n' % finish_dt.strftime('%b %d %H:%M:%S')
    result += 'URL: %s\n' % event['url'].strip()
    result += '----------------------------------------------------\n'
    return result

def event_grabber():
    """
        Возвращает список близжайших ctf'ов, которые будут идти в течение следующих 10 дней
    """
    timestamp_start, timestamp_finish = get_time_range()
    r = requests.get('https://ctftime.org/api/v1/events/?limit=100&start=%d&finish=%d' % (timestamp_start, timestamp_finish))
    events = r.json()
    parsed_events = []
    for e in events:
        parsed_events.append(parse_event(e))

    return ''.join(parsed_events)

if __name__ == '__main__':
    print event_grabber()
