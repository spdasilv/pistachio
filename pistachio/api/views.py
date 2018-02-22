from django.http import JsonResponse
from .scheduler import scheduleRun
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import Cities, Trip, Locations, Bid, UsersTrip, AuthUser, SelectedActivities, Hotels
from .forms import SignUpForm, NewTripForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views.generic.base import TemplateView
import json
import datetime
from ast import literal_eval as make_tuple


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/api/bidLocations')
    else:
        form = SignUpForm()
    return render(request, 'api/signup.html', {'form': form})


def parseFriends(friends):
    friendList = friends.split(';')
    return friendList


def newTrip(request):
    if request.method == 'POST':
        form = NewTripForm(request.POST)
        if form.is_valid():
            city_id = int(form.cleaned_data.get('city_choice'))
            owner_id = request.user.id
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            bidding_ends = form.cleaned_data.get('bidding_ends')
            created_at = datetime.datetime.now()
            new_trip = Trip(city_id=city_id, owner_id=owner_id, start_date=start_date, end_date=end_date, bidding_ends=bidding_ends, created_at=created_at)
            new_trip.save()

            new_usertrip = UsersTrip(user_id=owner_id, trip_id=new_trip.id, is_owner=True)
            new_usertrip.save()
            friends = parseFriends(form.cleaned_data.get('emails'))
            for friend in friends:
                user = AuthUser.objects.filter(email=friend).values('id').first()
                new_usertrip = UsersTrip(user_id=user['id'], trip_id=new_trip.id, is_owner=False)
                new_usertrip.save()
        else:
            error = form.errors
    return redirect('/api')


class bidLocationView(generic.ListView):
    template_name = 'api/bidLocations.html'
    context_object_name = 'locations'

    def get_queryset(self):
        return Locations.objects.filter(city_id=3).filter(user_study=True).all()

class dragDropView(generic.ListView):
    template_name = 'api/drag_drop.html'
    context_object_name = 'actDetails'

    def get_queryset(self):
        return Locations.objects.filter(selectedactivities__trip_id=self.kwargs['pk']).filter(rating__gte=9).all().order_by('-rating')


class selectActivitiesView(generic.DetailView):
    template_name = 'api/selectActivities.html'
    model = Trip

    def get_context_data(self, *, object_list=None, **kwargs):
        trip = Trip.objects.filter(pk=self.kwargs['pk']).values('id', 'city_id').first()
        context = super(selectActivitiesView, self).get_context_data(**kwargs)
        context['actDetails'] = Locations.objects.filter(city_id=trip['city_id']).filter(rating__gte=6).all().order_by(
            '-rating')
        return context

class adminGAView(TemplateView):
    template_name = 'api/adminGA.html'


class homeView(generic.ListView):
    template_name = 'api/home.html'
    model = Cities

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(homeView, self).get_context_data(**kwargs)
        context['trips'] = Trip.objects.filter(userstrip__user=self.request.user.id).all()
        return context


def hourTomin(date):
    offset = 0
    if date[0] == '+':
        offset = 1440
        date = date[1:]
    hour = int(date[0] + date[1])
    mins = int(date[2] + date[3])
    totalmins = hour*60 + mins + offset
    return totalmins


@csrf_exempt
def runGA(request):
    if request.is_ajax():
        body_string = request.body.decode('utf8').replace("'", '"')
        obj = json.loads(body_string)
        tripInfo = Trip.objects.filter(pk=obj['trip_id']).values('start_date', 'end_date').first()
        tripStart = tripInfo['start_date']
        tripEnd = tripInfo['end_date']
        tripLenght = (tripEnd - tripStart).days + 1
        days = {}
        for i in range(0, tripLenght):
            days[i] = {'weekday': (tripStart + datetime.timedelta(days=i)).weekday() + 1,
                       'start': 540,
                       'end': 1080
                       }
        bidSum = Bid.objects.filter(trip_id=obj['trip_id']).values('location_id').annotate(Sum('value')).all()
        locations = Locations.objects.filter(city_id=3).filter(user_study=True).all()
        if bidSum.exists():
            dict = {}
            dict[0] = {
                'id': 0,
                'lat': 51.495099,
                'lon': -0.183834,
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
                    't': location.visit_time,
                    'schedule': schedule
                }
        schedule = scheduleRun(dict, days)
        results = generateResponse(schedule, locations)
        response = {"response": results}
    else:
        response = {"response": "ERROR"}
    return JsonResponse(results)


@csrf_exempt
def bidAjax(request):
    if request.is_ajax():
        user_id = request.user.id
        body_string = request.body.decode('utf8').replace("'", '"')
        obj = json.loads(body_string)
        bids = convertToDict(obj['input'])
        for key, value in bids.items():
            bid = Bid(trip_id=int(obj['trip_id']), location_id=int(key), user_id=user_id, value=int(value['bid']))
            bid.save()
        results = {"response": "THANK YOU"}
    else:
        results = {"response": "ERROR"}
    return JsonResponse(results)


@csrf_exempt
def getHotels(request):
    if request.is_ajax():
        body_string = request.body.decode('utf8').replace("'", '"')
        obj = json.loads(body_string)
        city_id = obj['city_id']
        hotels = Hotels.objects.filter(city_id=city_id).all()
        hotels_response = []
        for hotel in hotels:
            hotels_response.append({'id': hotel.id, 'name': hotel.name})
        results = {"response": hotels_response}
    else:
        results = {"response": "ERROR"}
    return JsonResponse(results)


@csrf_exempt
def addActivitiesAjax(request):
    if request.is_ajax():
        result = {'response': None}
        body_string = request.body.decode('utf8').replace("'", '"')
        obj = json.loads(body_string)
        userInTrip = UsersTrip.objects.filter(trip_id=obj['trip_id']).filter(user_id=request.user.id).first()
        if userInTrip is not None:
            SelectedActivities.objects.filter(user_id=request.user.id).filter(trip_id=obj['trip_id']).delete()
            for activity in obj['activities']:
                selectedActivity = SelectedActivities(trip_id=obj['trip_id'],
                                                      user_id=request.user.id, location_id=activity)
                selectedActivity.save()
        result['response'] = 1
        return JsonResponse(result)


def convertToDict(list):
    dict = {}
    for item in list:
        dict[item['id']] = item
    return dict


def generateResponse(schedule, locations):
    response = {}
    for i, bucket in enumerate(schedule):
        for j, activity in enumerate(bucket.plan):
            location = locations.get(pk=activity[0])
            response[location.id] = {'activity_name': location.name}
    return response