from background_task import background
from logging import getLogger
from .scheduler import scheduleRun
from .models import Trip, Locations, Bid, ScheduleDetails, Schedules
from django.db.models import Sum
import datetime
from ast import literal_eval as make_tuple

logger = getLogger(__name__)


@background(schedule=30)
def checkTrips():
    print('Running...')
    trip = Trip.objects.filter(stage=3).first()
    if trip is not None:
        runGA(trip.id)
        trip.stage = 4
        trip.save(update_fields=['stage'])
        print('Trip Schedule Generated for ID ' + str(trip.id))
    else:
        print('No Stage 3 Trips!\n')

def runGA(trip_id):
    tripInfo = Trip.objects.filter(pk=trip_id).first()
    tripStart = tripInfo.start_date
    tripEnd = tripInfo.end_date
    tripLenght = (tripEnd - tripStart).days + 1
    days = {}
    for i in range(0, tripLenght):
        days[i] = {'weekday': (tripStart + datetime.timedelta(days=i)).weekday() + 1,
                   'start': 540,
                   'end': 1080
                   }
    bidSum = Bid.objects.filter(trip_id=trip_id).values('location_id').annotate(Sum('value')).all()
    locations = Locations.objects.filter(city_id=tripInfo.city_id).all()
    if bidSum.exists():
        hotel = tripInfo.hotel
        dict = {}
        dict[0] = {
            'id': 0,
            'lat': hotel.lat,
            'lon': hotel.lon,
            'w': 0,
            't': 0,
            'schedule': {
                1: (0, 1440),
                2: (0, 1440),
                3: (0, 1440),
                4: (0, 1440),
                5: (0, 1440),
                6: (0, 1440),
                7: (0, 1440)
            }
        }
        for bid in bidSum.iterator():
            location = locations.get(pk=bid['location_id'])
            avg_time = location.visit_time
            if avg_time is None:
                avg_time = 35
            times = location.schedule
            schedule = {}
            if times != '':
                times_list = times.split(";")
                for i, day in enumerate(times_list):
                    if i < len(times_list) - 1:
                        day_string = day.strip()
                    else:
                        day_string = day.strip()
                    day_info = make_tuple(day_string)
                    schedule[day_info[0]] = (hourTomin(day_info[1]), hourTomin(day_info[2]))
            dict[bid['location_id']] = {
                'id': bid['location_id'],
                'lat': location.lat,
                'lon': location.lon,
                'w': bid['value__sum'],
                't': avg_time,
                'schedule': schedule
            }
    schedule = scheduleRun(dict, days)
    generateResponse(schedule, locations, tripStart, trip_id)


def generateResponse(schedule, locations, start_date, trip_id):
    Schedules.objects.filter(trip_id=trip_id).delete()
    for i, bucket in enumerate(schedule):
        schedule = Schedules(trip_id=trip_id, day=start_date + datetime.timedelta(days=i))
        schedule.save()
        for j, activity in enumerate(bucket.plan):
            location = locations.get(pk=activity[0])
            schedule_detail = ScheduleDetails(schedule_id=schedule.id, activity_id=location.id, activity_order=j,
                                              activity_name=location.name, activity_starts=minToHour(activity[1]),
                                              activity_ends=minToHour(activity[1] + activity[2]),
                                              activity_lat=activity[3], activity_lon=activity[4])
            schedule_detail.save()


def hourTomin(date):
    offset = 0
    if date[0] == '+':
        offset = 1440
        date = date[1:]
    hour = int(date[0] + date[1])
    mins = int(date[2] + date[3])
    totalmins = hour*60 + mins + offset
    return totalmins


def minToHour(min):
    hour = int(min/60)
    hour_str = ''
    if hour < 10:
        hour_str += '0'
    hour_str += str(hour)

    minutes_str = ''
    minutes = min - hour*60
    if minutes < 10:
        minutes_str += '0'
    minutes_str += str(minutes)

    return hour_str + ':' + minutes_str