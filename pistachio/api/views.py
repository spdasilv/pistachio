from django.http import JsonResponse
from .scheduler import scheduleRun
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import Cities, Trip
from .forms import SignUpForm, NewTripForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import json
import  datetime


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/api/selectCity.html')
    else:
        form = SignUpForm()
    return render(request, 'api/signup.html', {'form': form})


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
            return redirect('/api/selectCity')
    else:
        form = NewTripForm()
    return render(request, 'api/newTrip.html', {'form': form})


class selectCityView(generic.ListView):
    template_name = 'api/selectCity.html'
    context_object_name = 'cities'

    def get_queryset(self):
        return Cities.objects.all()


class createTripView(generic.DetailView):
    model = Cities
    template_name = 'api/createTrip.html'


@csrf_exempt
def requestAjax(request):
    if request.is_ajax():
        body_string = request.body.decode('utf8').replace("'", '"')
        obj = json.loads(body_string)
        obj_dict = convertToDict(obj)
        schedule = scheduleRun(obj_dict)
        results = generateResponse(schedule)
    else:
        results = "ERROR"
    return JsonResponse(results)


def convertToDict(list):
    dict = {}
    for item in list:
        dict[item['id']] = item
    return dict


def generateResponse(schedule):
    response = {}
    for i, bucket in enumerate(schedule):
        day = {}
        for j, activity in enumerate(bucket.plan):
            day['activity_' + str(j + 1)] = {'start_time': activity[1], 'activity_id': activity[0]}
        response['day_' + str(i + 1)] = day
    return response
