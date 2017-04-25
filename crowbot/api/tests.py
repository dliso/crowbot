from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.urls import reverse
import json, requests, pickle
from api.views import *
from backend.models import Course, Question, Answer
from . import views
from .messagetype import MESSAGETYPE

# Create your tests here.

class ApiViewTests(TestCase):
    def setUp(self):
        Course.objects.create(code='TDT4140', name='Software Engineering',
                              recommended_previous_knowledge='Subjects TDT4100 Object-Oriented Programming and TDT4120 Algorithms and Data Structures, or equivalent.',
                              required_previous_knowledge='',exam_date=None,exam_support_code='',exam_support_name='',location='Trondheim',
                              semester='Spring',teacher_name='Pekka Kalevi Abrahamsson',teacher_email='pekka.abrahamsson@ntnu.no',ects_credits=7.50)

        Course.objects.create(code='EXPH0004',name='Examen philosophicum for Science and Technology',recommended_previous_knowledge='',required_previous_knowledge='',
                              #litt usikker på denne måten å spesifisere en dato variabel på
                              exam_date='2017-05-27',exam_support_code='D',
                              exam_support_name='No written or handwritten examination support material is permitted. Specified simple calculator is permitted.',
                              location='Trondheim',
                              semester='Autumn and Spring',teacher_name='Erling Skjei',teacher_email='erling.skjei@ntnu.no',ects_credits=7.50)

        Question.objects.create(text='How many exercises is mandatory in TDT4140?',
                                course=Course.objects.get(code='TDT4140'),
                                lemma=pickle.dumps(['exercise', 'tdt4140']))

        Question.objects.create(text='How many exercises is there in total in EXPH0004?',
                                course=Course.objects.get(code='EXPH0004'),
                                lemma=pickle.dumps(['exercise', 'exph0004']))

        Answer.objects.create(question = Question.objects.get(text = 'How many exercises is mandatory in TDT4140?'),
                              text = 'No exercises in TDT4140, just a mandatory project.')

        User.objects.create(username='crowcrow', password='crowcrow123')
        User.objects.create(username='crowcrow2', password='crowcrow12321')

    def test_add_course_view_status_code(self):
        response = self.client.get(reverse('backend:add_course'))
        self.assertEqual(response.status_code, 200)

    def test_add_course_view_response(self):
        response = self.client.get(reverse('backend:add_course'))
        self.assertContains(response,"Send POST requests here to add courses to the database.")

    def test_add_question(self):
        question = 'When is the exam in TMA4100?'
        add_question(question)
        self.assertEqual(Question.objects.all().count(), 3)

    def test_make_message_stored_question(self):
        response = make_message(User.objects.get(username='crowcrow'), Question.objects.get(text='How many exercises is mandatory in TDT4140?'))
        self.assertEqual(response.get('msgType'), 'StoredQuestion')

    def test_make_message_stored_answer(self):
        response = make_message(User.objects.get(username='crowcrow'), Answer.objects.get(question = Question.objects.get(text = 'How many exercises is mandatory in TDT4140?')))
        self.assertEqual(response.get('msgType'), 'StoredAnswer')

    def test_make_feed_item(self):
        response = make_feed_item('question', 'Hello?', ['Hi', 'Good day!'])
        self.assertEqual(response, {'itemType': 'question',
            'firstMessage': 'Hello?',
            'replies': ['Hi', 'Good day!']})

class SimpleTest(TestCase):
    fixtures = ['fixtures/backend.Course.json']
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='unittestman',
            email='unit@test.man',
            password='unguessable',
        )

    def test_subscribe_to_existing_course(self):
        request = self.factory.get('/api/subscribe_to/')
        request.user = self.user
        response = views.subscribe_to_course(request, 'tma4110')
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_add_unseen_question(self):
        request = self.factory.post('/api/ask_question')
        request.user = self.user
        request.POST['body'] = 'TMA4100 Who does the thing with the dancing?'
        response = views.respond_to_message(request)
        res = json.loads(response.content)
        print(res)
        self.assertEqual(res[0]['msgType'], MESSAGETYPE.bot_response)
        self.assertTrue('No similar question detected' in res[0]['msgBody'])

    def test_similar_question(self):
        request = self.factory.post('/api/ask_question')
        request.user = self.user
        request.POST['body'] = 'TMA4100 Who does the thing with the dancing?'
        response = views.respond_to_message(request)
        res = json.loads(response.content)
        print(res)
        self.assertTrue(True)
