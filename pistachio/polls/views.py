from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Choice, Question
from .scheduler import scheduleRun
from django.shortcuts import get_object_or_404, render, render_to_response
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class viewAjax(generic.TemplateView):
    template_name = 'polls/viewAjax.html'


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
