from django.http import JsonResponse
from .scheduler import scheduleRun
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import Cities, Trip, Locations, Bid, UsersTrip, AuthUser, SelectedActivities
from .forms import SignUpForm, NewTripForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views.generic.base import TemplateView
import json
import datetime


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
            city_id = Cities.objects.filter(name=form.cleaned_data.get('city_choice')).values('id').first()
            owner_id = request.user.id
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            bidding_ends = form.cleaned_data.get('bidding_ends')
            created_at = datetime.datetime.now()
            new_trip = Trip(city_id=city_id['id'], owner_id=owner_id, start_date=start_date, end_date=end_date, bidding_ends=bidding_ends, created_at=created_at)
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


def addActivities(request):
    if request.is_ajax():
        body_string = request.body.decode('utf8').replace("'", '"')
        obj = json.loads(body_string)
        trip = Trip.objects.filter(pk=obj['trip_id']).filter(userstrip__user=request.user.id).values('id').first()
        if 'id' in trip:
            SelectedActivities.objects.filter(user_id=request.user.id).filter(trip_id=trip['id']).delete()
            for activity in obj['activities']:
                selectedActivity = SelectedActivities(trip_id=trip['id'], user_id=request.user.id, location_id=activity['id'])
                selectedActivity.save()
    return redirect('/api')


class selectCityView(generic.ListView):
    template_name = 'api/selectCity.html'
    context_object_name = 'cities'

    def get_queryset(self):
        return Cities.objects.all()


class bidLocationView(generic.ListView):
    template_name = 'api/bidLocations.html'
    context_object_name = 'locations'

    def get_queryset(self):
        return Locations.objects.filter(city_id=3).filter(user_study=True).all()

class activityDetailsView(generic.ListView):
    template_name = 'api/activityDetails.html'
    context_object_name = 'actDetails'

    def get_queryset(self):
        trip = Trip.objects.filter(pk=self.kwargs['pk']).values('city_id').first()
        return Locations.objects.filter(city_id=trip['city_id']).filter(rating__gte=6).all().order_by('-rating')


class adminGAView(TemplateView):
    template_name = 'api/adminGA.html'


class homeView(generic.ListView):
    template_name = 'api/home.html'
    # Name object
    context_object_name = 'trips'

    # Define object aka query from DB
    def get_queryset(self):
        #pulling from table TRIP, filtering over table usertrip column user that equals self.request.user.id (active user)
        return Trip.objects.filter(userstrip__user=self.request.user.id).all()

class dragDropView(generic.ListView):
    template_name = 'api/drag_drop.html'
    context_object_name = 'cities'

    def get_queryset(self):
        #pulling from table TRIP, filtering over table usertrip column user that equals self.request.user.id (active user)
        return Cities.objects.all()

@csrf_exempt
def runGA(request):
    if request.is_ajax():
        body_string = request.body.decode('utf8').replace("'", '"')
        obj = json.loads(body_string)
        bidSum = Bid.objects.filter(trip_id=obj['trip_id']).values('location_id').annotate(Sum('value')).all()
        locations = Locations.objects.filter(city_id=3).filter(user_study=True).all()
        if bidSum.exists():
            dict = {}
            dict[0] = {
                'id': 0,
                'lat': 51.495099,
                'lon': -0.183834,
                'w': 0,
                't': 0
            }
            for bid in bidSum.iterator():
                location = locations.get(pk=bid['location_id'])
                dict[bid['location_id']] = {
                    'id': bid['location_id'],
                    'lat': location.lat,
                    'lon': location.lon,
                    'w': bid['value__sum'],
                    't': location.visit_time
                }
        schedule = scheduleRun(dict)
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


class createTripView(generic.DetailView):
    model = Cities
    template_name = 'api/createTrip.html'


@csrf_exempt
def requestAjax(request):
    id = request.user.id
    if request.is_ajax():
        body_string = request.body.decode('utf8').replace("'", '"')
        obj = json.loads(body_string)
        obj_dict = convertToDict(obj)
        schedule = scheduleRun(obj_dict)
        results = generateResponse(schedule)
    else:
        results = "ERROR"
    return JsonResponse(results)

@csrf_exempt
def getTrips(request):
    return JsonResponse({"key": 0})


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