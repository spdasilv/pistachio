from django.http import JsonResponse
from .scheduler import scheduleRun
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import Cities, Locations
import json


class viewAjax(generic.TemplateView):
    template_name = 'api/viewAjax.html'


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
