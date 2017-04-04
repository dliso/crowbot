import json

from django.utils import timezone as tz
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core import exceptions

from backend.models import Course, Question, Answer

from apiai_connection import crowbot_chat

from account_system.models import Profile

from .usertype import *
from .messagetype import *

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
    courses = request.user.profile.subscribed_courses.all().values('code')
    courses = [c['code'] for c in courses]
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

def make_feed_item(item_type, first_message, replies=[]):
    return {'itemType': item_type,
            'firstMessage': first_message,
            'replies': replies}

def user_feed(request):
    """
    Return the following:
    1. All questions and answers connected to a course
    """
    feed = []
    courses = request.user.profile.subscribed_courses.values('code')
    for course in courses:
        print(course['code'])
        qs = Question.objects.filter(course__code = course['code'])
        for q in qs:
            print(q)
            profile = q.user_id.profile
            if profile:
                user = profile.to_dict()
            else:
                user = {}
            firstMessage = {
                    'user': user,
                    'ownMessage': request.user == q.user_id,
                    'timestamp': q.creation_datetime,
                    'msgBody': q.text,
                    'courseId': q.course.code,
                    'pk': q.id,
                    'thisUserAsked': False,
                    'askedCount': q.interested_users.count(),
                    'msgType': MESSAGETYPE.stored_question,
                }
            replies = []
            for a in q.answers.all():
                print(a.text)
                reply = {
                    'user': a.user_id.profile.to_dict(),
                    'ownMessage': a.user_id == request.user,
                    'timestamp': a.creation_datetime,
                    'msgBody': a.text,
                    'courseId': a.question.course.code,
                    'pk': a.id,
                    'score': a.upvoted_by.all().count() - a.downvoted_by.all().count(),
                    'thisUserVoted': ANSWERVOTE.none,
                    'msgType': MESSAGETYPE.stored_answer,
                }
                replies.append(reply)
            feed.append({
                'itemType': FEEDITEMTYPE.question,
                'replies': replies,
                'firstMessage': firstMessage,
            })
    return HttpResponse(json_dump(feed))

@csrf_exempt
def subscribe_to_course(request, course_id):
    print(course_id)
    if request.user.is_authenticated:
        profile = request.user.profile
        print(profile)
        print(profile.subscribed_courses)
        try:
            course = Course.objects.get(code__iexact = course_id)
            profile.subscribed_courses.add(course)
            print(course)
            return HttpResponse('subscribed')
        except exceptions.ObjectDoesNotExist as e:
            return HttpResponse('Course does not exist', status=404)
    else:
        return HttpResponse('must be logged in to subscribe to courses', status=403)

def unsubscribe_from_course(request, course_id):
    if request.user.is_authenticated:
        try:
            course = Course.objects.get(code__iexact = course_id)
        except exceptions.ObjectDoesNotExist as e:
            return HttpResponse('Course does not exist', status=404)

        request.user.profile.subscribed_courses.remove(course)
        return HttpResponse('unsubscribed')
    else:
        return HttpResponse('must be logged in to unsubscribe from courses', status=403)

@csrf_exempt
def plus_one_question(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        pk = request.POST['pk']
        try:
            q = Question.objects.get(id=pk)
        except exceptions.ObjectDoesNotExist as e:
            return HttpResponse("question doesn't exist")
        print(request.POST)
        return HttpResponse('thanks')
    else:
        return HttpResponse('must be logged in to +1 question')

