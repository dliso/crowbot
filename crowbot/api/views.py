import json

from django.utils import timezone as tz
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core import exceptions

from backend.models import Course, Question, Answer, ChatLog

from apiai_connection import crowbot_chat

from account_system.models import Profile

from .usertype import *
from .messagetype import *
from .answervote import *

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

bot_user = {
    'usertype': USERTYPE.bot,
    'name': 'Crowbot',
    'avatarUrl': 'crowbot.png'
}

def make_message(user, obj):
    msgType = MESSAGETYPE.stored_question if isinstance(obj, Question) else MESSAGETYPE.stored_answer
    msg = {
        'user': user.profile.to_dict() if user is not None else None,
        'msgBody': obj.text,
        'msgType': msgType,
        'ownMessage': False,
        'timestamp': obj.creation_datetime,
        'pk': obj.id,
    }
    if msgType == MESSAGETYPE.stored_answer:
        msg['courseId'] = obj.question.course.code
        msg['score'] = obj.score()
        msg['thisUserVoted'] = obj.user_voted(user)
    else:
        msg['courseId'] = obj.course.code
        msg['askedCount'] = obj.times_asked()
        msg['thisUserAsked'] = obj.did_user_ask(user)
    return msg

@csrf_exempt
def respond_to_message(request):
    if request.method != 'POST':
        return HttpResponse('only POST accepted', status=405)
    user = request.user
    ChatLog.record_user_message(request.POST['body'], user)
    responses = []
    bot_response = crowbot_chat.ask_apiai(request.POST['body'],
                                          request.user)

    # Wrap the bot response in a list if it isn't one
    if not isinstance(bot_response, list):
        bot_response = [bot_response]

    for message in bot_response:
        if isinstance(message, str):
            user = bot_user
            msgBody = message
            res = {
                'user': user,
                'msgBody': msgBody,
                'msgType': MESSAGETYPE.bot_response,
                'ownMessage': False,
                'courseId': None,
                'pk': None,
            }
            responses.append(res)
        else:
            msgBody = message['body']
            obj = message['obj']
            user = obj.user_id
            res = make_message(user, obj)
            responses.append(res)

    for msg in responses:
        ChatLog.record_stored_object(msg, request.user)

    return HttpResponse(json_dump(responses), content_type='application/json')

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
    # text = req_body['body'].split(' ', maxsplit=1)[1]
    text = req_body['body']
    ans = Answer(
        question = Question.objects.get(pk=req_body['q_pk']),
        text = text,
        user_id = request.user,
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

def make_feed_item(item_type, first_message, replies=[]):
    return {'itemType': item_type,
            'firstMessage': first_message,
            'replies': replies}

def user_feed(request):
    """
    Return the following:
    1. All questions and answers connected to a course
       - TODO Change to all questions asked by current user
    2. Info messages, ie. answers without questions
    3. FAQs, ie. questions asked by more than 1 person
    4. Highly rated answers
    """
    feed = []
    courses = request.user.profile.subscribed_courses.values('code')
    for course in courses:
        print(course['code'])
        qs = Question.objects.filter(course__code = course['code'])
        for q in qs:
            print(q)
            profile = None
            if q.user_id:
                profile = q.user_id.profile
            user = {}
            if profile:
                user = profile.to_dict()
            firstMessage = q.to_dict(request.user)
            replies = []
            for a in q.answers.all():
                print(a.text)
                reply = a.to_dict(request.user)
                replies.append(reply)
            feed.append({
                'itemType': FEEDITEMTYPE.question,
                'replies': replies,
                'firstMessage': firstMessage,
            })
    return HttpResponse(json_dump(feed), content_type='application/json')

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
            return HttpResponse('subscribed to ' + course.code)
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
        user = profile.user
        pk = request.POST['pk']
        try:
            q = Question.objects.get(id=pk)
        except exceptions.ObjectDoesNotExist as e:
            return HttpResponse(json_dump(
                {'status': 'failure'}
            ), content_type='application/json')
        print(request.POST)
        was_interested = q.did_user_ask(user)
        is_interested = not was_interested
        if was_interested:
            q.interested_users.remove(user)
        else:
            q.interested_users.add(user)
        num_interested = q.interested_users.count()
        return HttpResponse(
            json_dump({'askedCount': num_interested,
                       'status': 'success',
                       'thisUserAsked': is_interested}),
            content_type='application/json'
        );
    else:
        return HttpResponse('must be logged in to +1 question')

@csrf_exempt
def vote_on_answer(request):
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile
        pk = request.POST['pk']
        clicked_button = request.POST['button']
        try:
            ans = Answer.objects.get(id=pk)
        except exceptions.ObjectDoesNotExist as e:
            return HttpResponse(json_dump(
                {'status': 'failure'}
            ), content_type='application/json')

        new_vote = ans.vote(user, clicked_button)

        return HttpResponse(json_dump({
            'status': 'success',
            'score': ans.score(),
            'vote': new_vote,
        }), content_type='application/json')
    else:
        return HttpResponse('must be logged in to vote on questions')


def chat_log(request):
    if not request.user.is_authenticated:
        return HttpResponse('must be logged in to retrieve chat log')
    user = request.user
    chatlog = ChatLog.objects.filter(user_id=user)
    log = [m.format(user) for m in chatlog]
    return HttpResponse(json_dump(log), content_type='application/json')


def courses_matching(request, course_name_fragment):
    if len(course_name_fragment) < 2:
        return HttpResponse('fragment to match must contain at least 2 characters')
    courses_matching_name = Course.objects.filter(name__icontains=course_name_fragment)
    courses_matching_code = Course.objects.filter(code__icontains=course_name_fragment)
    courses = list(set(courses_matching_code).union(set(courses_matching_name)))
    return HttpResponse(json_dump(
        [{'code': c.code, 'name': c.name} for c in courses]
    ), content_type='application/json')
