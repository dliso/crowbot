import json

from django.utils import timezone as tz
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
        res_data = {
            'usertype': 'bot',
            'username': 'Crowbot',
        }
        if req_body[0] == '!':
            add_question(req_body[1:])
            res_data['body'] = 'Your question was added to the manual review queue.'
        elif req_body == 'test bot message':
            res_data['usertype'] = 'bot'
            res_data['username'] = 'Crowbot'
            res_data['body'] = 'beep boop boop boop'
        elif req_body == 'test prof message':
            res_data['usertype'] = 'professor'
            res_data['username'] = 'Dr. Crowbot'
            res_data['body'] = 'Slik ser et professor-svar ut.'
        elif req_body == 'test student message':
            res_data['usertype'] = 'student'
            res_data['username'] = 'Testleif'
            res_data['body'] = 'bla bla bla'
        elif req_body == 'test anon message':
            res_data['usertype'] = ''
            res_data['username'] = ''
            res_data['body'] = 'jeg tør ikke oppgi navnet mitt'
        else:
            res_data['body'] = str(crowbot_chat.ask_apiai(req_body))
    return HttpResponse(json.dumps(res_data), content_type="application/json")

def questions_for_course(request, course_code):
    questions = Question.objects.all().values('text', 'creation_datetime')
    for q in questions:
        q['datetime'] = str(q.pop('creation_datetime'))
    return HttpResponse(json.dumps(list(questions), cls=serializers.json.DjangoJSONEncoder), content_type='application/json')
