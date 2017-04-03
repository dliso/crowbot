import json

from django.utils import timezone as tz
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from backend.models import Course, Question, Answer

from apiai_connection import crowbot_chat

# Create your views here.
json_dump = lambda data: json.dumps(data, cls=serializers.json.DjangoJSONEncoder)


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
    if request.method != 'POST':
        return HttpResponse('only POST accepted', status=405)
    print(request)
    if request.method == 'POST':
        req_body = request.POST['body']
        res_data = {
            'usertype': 'bot',
            'username': 'Crowbot',
        }
        # Handle special commands:
        if req_body[0] == '!':
            add_question(req_body[1:])
            res_data['body'] = 'Your question was added to the manual review queue.'
        elif req_body == 'test bot':
            res_data['usertype'] = 'bot'
            res_data['username'] = 'Crowbot'
            res_data['body'] = 'beep boop boop boop'
        elif req_body == 'test prof':
            res_data['usertype'] = 'instructor'
            res_data['username'] = 'Dr. Crowbot'
            res_data['body'] = 'Slik ser et professor-svar ut.'
            res_data['timestamp'] = tz.now()
        elif req_body == 'test student':
            res_data['usertype'] = 'student'
            res_data['username'] = 'Testleif'
            res_data['body'] = 'bla bla bla'
            res_data['timestamp'] = tz.now()
        elif req_body == 'test anon':
            res_data['usertype'] = ''
            res_data['username'] = 'Unknown'
            res_data['body'] = 'jeg tør ikke oppgi navnet mitt'
            res_data['timestamp'] = tz.now()
        elif req_body == 'test multi':
            res_data['body'] = 'multibeskjed'
            res_data['timestamp'] = tz.now()
            res_data = [res_data] * 3
        else:
            response = crowbot_chat.ask_apiai(req_body)
            res_data['body'] = response
            if isinstance(response, list):
                res_data = response
    if not isinstance(res_data, list):
        res_data = [res_data]
    return HttpResponse(json_dump(res_data), content_type="application/json")

def questions_for_course(request, course_code):
    questions = Question.objects.filter(
        course__code=course_code.upper()
    ).values('text', 'creation_datetime', 'pk')
    for q in questions:
        q['datetime'] = str(q.pop('creation_datetime'))
    return HttpResponse(json_dump(list(questions)), content_type='application/json')

def my_courses(request):
    courses = ['tdt4145', 'tdt4140', 'tma4100', 'tdt4195', 'tma4110']
    return HttpResponse(json_dump(list(courses)), content_type='application/json')

@csrf_exempt
def submit_answer(request):
    print(request.POST)
    req_body = request.POST
    text = req_body['body'].split(' ', maxsplit=1)[1]
    ans = Answer(
        question = Question.objects.get(pk=req_body['q_pk']),
        text = text
    )
    ans.save()
    response = {
        'body': 'Answer received.'
    }
    return HttpResponse(json_dump(response), content_type='application/json')

@csrf_exempt
def answers_for_question(request, pk):
    response = Answer.objects.filter(question__exact=pk)
    return HttpResponse(
        serializers.serialize('json', response)
    )

class USERTYPE:
    bot        = 'Bot'
    instructor = 'Instructor'
    student    = 'Student'
    anonymous  = 'Anonymous'

class FEEDITEMTYPE:
    question              = 'Question'
    question_with_answers = 'QuestionWithAnswers'
    faq                   = 'FAQ'
    info                  = 'Info'
    highly_rated          = 'HighlyRated'

class ANSWERVOTE:
    none = 'none'
    up   = 'up'
    down = 'down'

class MESSAGETYPE:
    bot_response    = 'BotResponse'
    stored_question = 'StoredQuestion'
    stored_answer   = 'StoredAnswer'

def make_feed_item(item_type, first_message, replies=[]):
    return {'itemType': item_type,
            'firstMessage': first_message,
            'replies': replies}

def user_feed(request):
    u1 = {
        'pk': 1,
        'name': 'Student Smith',
        'usertype': USERTYPE.student,
        'avatarUrl': '',
    }
    u2 = {
        'pk': 2,
        'name': 'Dr. Teacher',
        'usertype': USERTYPE.instructor,
        'avatarUrl': '',
    }
    feed = []
    question = make_feed_item(FEEDITEMTYPE.question,
                              {
                                  'user': u1,
                                  'ownMessage': False,
                                  'timestamp': tz.now(),
                                  'msgBody': 'hjølp',
                                  'courseId': 'TDT4145',
                                  'pk': 1,
                                  'thisUserAsked': False,
                                  'askedCount': 10,
                                  'msgType': MESSAGETYPE.stored_question,
                              })
    feed.append(question)
    answer = {
        'user': u2,
        'ownMessage': False,
        'timestamp': tz.now(),
        'msgBody': 'hjølp',
        'courseId': 'TDT4145',
        'pk': 1,
        'score': 5,
        'thisUserVoted': ANSWERVOTE.none,
        'msgType': MESSAGETYPE.stored_answer,
    }
    q_with_as = make_feed_item(FEEDITEMTYPE.question_with_answers,
                               question['firstMessage'],
                               [answer]
    )
    feed.append(q_with_as)
    return HttpResponse(json_dump(feed))
