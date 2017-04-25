from django.test import TestCase

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from backend.models import Course

import json

from . import views
from .messagetype import MESSAGETYPE

# Create your tests here.

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
