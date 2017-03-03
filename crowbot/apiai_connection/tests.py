from django.test import TestCase
import json, apiai
from apiai_connection.crowbot_chat import *
from backend.models import Course

CLIENT_ACCESS_TOKEN = '1b0f421f4b1045c5a9b29c8372573383'


# Create your tests here.
class TestCrowbotChat(TestCase):
    def setUp(self):
        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

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

        Course.objects.create(code='FE8111',name='Molecular Beam Epitaxy',
                              recommended_previous_knowledge='TFE4145 Semiconductor Physics and Electronic Devices, Introduction, and TFE4180 Semiconductor Manufactoring Technology, or equivalent knowledge, will give an advantage.',
                              required_previous_knowledge='',
                              exam_date=None,exam_support_code='D',exam_support_name='No written or handwritten examination support material is permitted. Specified simple calculator is permitted.',
                              location='Trondheim',
                              semester='Autumn and Spring',teacher_name='Bjørn-Ove Fimland',teacher_email='bjorn.fimland@ntnu.no',ects_credits=7.50)
        #lage eksempel database objekter


    def load_text_request_with_query(self, query):

        request = self.ai.text_request()
        request.query = query
        request.query = request.query.upper()
        response = request.getresponse().read().decode('utf-8')
        return json.loads(response)




    def test_crowbot_understanding_course(self):
        query = 'How much credit do I get in tdt4105?'
        response = self.load_text_request_with_query(query)
        #result = response['result']
        code = response['result']['parameters']['course'''].upper()
        self.assertEqual(code, 'TDT4105')
        #self.assertEqual(course.ects_credits, 7.50)

    def test_crowbot_understanding_action(self):
        query = 'How much credit do I get in TMA4100?'
        response = self.load_text_request_with_query(query)
        #result = response['result']
        action = response['result']['action']
        self.assertEqual(action, 'find_credit')

    # def test_(self):
    #     self.assertEqual(1,1)



