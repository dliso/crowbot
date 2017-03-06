import json

from django.utils import timezone as tz
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from backend.models import Course, Question

from apiai_connection import crowbot_chat

# Create your views here.

@csrf_exempt
def add_course(request):
    if request.method == 'POST':
        print(request.body.decode())
        # The deserializer needs to know which model to use. We wrap the req.
        # body in the necessary JSON here.
        wrapped = '[{"model": "backend.course", "fields": %s}]' % request.body.decode()
        for d in serializers.deserialize('json', wrapped):
            d.save()
        return HttpResponse('Added %s to the database.' % d.object.code)
    else:
        return HttpResponse('Send POST requests here to add courses to the database.')

def add_question(question):
    q = Question(text=question)
    q.save()

@csrf_exempt
def respond_to_message(request):
    print(request)
    res = ''
    if request.method == 'GET':
        res += 'GET'
        for i in request.GET.items():
            res += str(i)
        res += '\n'
        res += str(crowbot_chat.ask_apiai(request.GET['q']))
    if request.method == 'POST':
        res += 'POST request received'
        req_body = request.POST['body']
        res_data = {}
        if req_body[0] == '!':
            add_question(req_body[1:])
            res_data['body'] = 'Your question was added to the manual review queue.'
        else:
            res_data['body'] = str(crowbot_chat.ask_apiai(req_body))
    return HttpResponse(json.dumps(res_data), content_type="application/json")

def questions_for_course(request, course_code):
    questions = [
        {'text': 'må jeg ta eksamen hvis jeg ikke har lyst?',
         'datetime': tz.now()},
        {'text': 'er det lov å koke???',
         'datetime': tz.now()},
    ]
    return HttpResponse(json.dumps(questions, cls=serializers.json.DjangoJSONEncoder), content_type='application/json')
