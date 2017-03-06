from django.test import TestCase
import json, apiai, datetime
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

#test course with nothing saved in database except required prev knowledge
        Course.objects.create(code='YRT5678',name='Tulle Emne',
                              recommended_previous_knowledge='', required_previous_knowledge='YRT6789 Tulle Emne 0,5',
                              exam_date=None,exam_support_code='',exam_support_name='',
                              location='',semester='',teacher_name='',
                              teacher_email='',ects_credits=None)



    def load_text_request_with_query(self, query):

        request = self.ai.text_request()
        request.query = query
        request.query = request.query.upper()
        response = request.getresponse().read().decode('utf-8')
        return json.loads(response)


#tester for å sjekke forståelsen til api.ai
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


#tester for å hente informasjon ut fra databasen
    def test_get_credit(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.ects_credits,7.50)
        self.assertEqual(EXPHIL.ects_credits, 7.50)
        self.assertEqual(MBE.ects_credits, 7.50)

    def test_get_exam_date(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.exam_date, None)
        self.assertEqual(EXPHIL.exam_date, datetime.date(2017, 5, 27))
        self.assertEqual(MBE.exam_date, None)

    def test_get_location(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.location, 'Trondheim')
        self.assertEqual(EXPHIL.location, 'Trondheim')
        self.assertEqual(MBE.location, 'Trondheim')

    def test_get_professor_name(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.teacher_name, 'Pekka Kalevi Abrahamsson')
        self.assertEqual(EXPHIL.teacher_name, 'Erling Skjei')
        self.assertEqual(MBE.teacher_name, 'Bjørn-Ove Fimland')

    def test_get_professor_email(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.teacher_email, 'pekka.abrahamsson@ntnu.no')
        self.assertEqual(EXPHIL.teacher_email, 'erling.skjei@ntnu.no')
        self.assertEqual(MBE.teacher_email, 'bjorn.fimland@ntnu.no')

    def test_get_semester(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.semester, 'Spring')
        self.assertEqual(EXPHIL.semester, 'Autumn and Spring')
        self.assertEqual(MBE.semester, 'Autumn and Spring')

    def test_get_exam_support_code(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.exam_support_code, '')
        self.assertEqual(EXPHIL.exam_support_code, 'D')
        self.assertEqual(MBE.exam_support_code, 'D')

    def test_get_exam_support_name(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.exam_support_name, '')
        self.assertEqual(EXPHIL.exam_support_name, 'No written or handwritten examination support material is permitted. Specified simple calculator is permitted.')
        self.assertEqual(MBE.exam_support_name, 'No written or handwritten examination support material is permitted. Specified simple calculator is permitted.')

    def test_get_recommended_previous_knowledge(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.recommended_previous_knowledge, 'Subjects TDT4100 Object-Oriented Programming and TDT4120 Algorithms and Data Structures, or equivalent.')
        self.assertEqual(EXPHIL.recommended_previous_knowledge,'')
        self.assertEqual(MBE.recommended_previous_knowledge,'TFE4145 Semiconductor Physics and Electronic Devices, Introduction, and TFE4180 Semiconductor Manufactoring Technology, or equivalent knowledge, will give an advantage.')

    def test_get_required_previous_knowledge(self):
        PU = Course.objects.get(code='TDT4140')
        EXPHIL = Course.objects.get(code='EXPH0004')
        MBE = Course.objects.get(code='FE8111')
        self.assertEqual(PU.required_previous_knowledge, '')
        self.assertEqual(EXPHIL.required_previous_knowledge,'')
        self.assertEqual(MBE.required_previous_knowledge,'')



#tester funksjoner i crowbot_chat

    #test for course with credit stored
    def test_user_request_credit(self):
        query = 'How much credit do I get in tdt4140?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output,'Credits for TDT4140 Software Engineering is 7.50')

    #test for course with no credit stored
    def test_user_request_credit_none(self):
        query = 'How much credit do I get in yrt5678?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output,'No information about credits in this course, YRT5678 Tulle Emne')


    #test for course with exam date stored
    def test_user_request_exam_date(self):
        query = 'When is the exam in exph0004?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output,'Exam date for EXPH0004 Examen philosophicum for Science and Technology is 27/05/2017')

    #test for course with no exam date
    def test_user_request_exam_date_none(self):
        query = 'When is the exam in tdt4140?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output,"No info about the exam in this course TDT4140 Software Engineering")


    #test for course with location stored
    def test_user_request_location(self):
        query = 'Where is FE8111 taught?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output,'FE8111 Molecular Beam Epitaxy is taught in Trondheim')

    #test for course with no location stored
    def test_user_request_location_none(self):
        query = 'Where is YRT5678 taught?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output,'No location information for YRT5678 Tulle Emne')


    #test for course with professor name stored
    def test_user_request_professor_name(self):
        query = 'Who is teaching FE8111?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output,'FE8111 Molecular Beam Epitaxy is taught by Bjørn-Ove Fimland')

    #test for course with no professor name stored
    def test_user_request_professor_name_none(self):
        query = 'Who is teaching YRT5678?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output,'No information about the lecturer in YRT5678 Tulle Emne')


    #test for course with both teacher name and email
    def test_user_request_professor_mail(self):
        query = 'How can I reach the professor in FE8111?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'FE8111 Molecular Beam Epitaxy is taught by Bjørn-Ove Fimland. They can be reached at bjorn.fimland@ntnu.no')

    #test for course with no teacher name or teacher email
    def test_user_request_professor_mail_none(self):
        query = 'How can I reach the professor in YRT5678?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'No information about the professors email in YRT5678 Tulle Emne')

    #TODO: test for course with teacher name, but no teacher email

    #TODO: test for course with no teacher name, but teacher email


    #test for course with semester info
    def test_user_request_semester(self):
        query = 'In what term is EXPH0004 taught?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'EXPH0004 Examen philosophicum for Science and Technology is taught in the Autumn and Spring')

    #test for course with no semester info
    def test_user_request_semester_none(self):
        query = 'In what term is yrt5678 taught?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'No information about semesters in YRT5678 Tulle Emne')


    #test course with both exam support code and name
    def test_user_request_exam_aids(self):
        query = 'What examination support is permitted in EXPH0004?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'Exam support materials for EXPH0004 Examen philosophicum for Science and Technology is code D: No written or handwritten examination support material is permitted. Specified simple calculator is permitted.')

    #test course with no exam support code or exam support name
    def test_user_request_exam_aids_none(self):
        query = 'What exam aids is permitted in TDT4140?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'No information about examination support in TDT4140 Software Engineering')

    #TODO: test course with exam support code, but no exam support name

    #TODO: test course with exam support name, but no exam support code

    #test course with needed prev knowledge stored
    def test_user_request_needed_knowledge(self):
        query = 'What required previous knowledge is there in YRT5678?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'Required previous knowledge is: YRT6789 Tulle Emne 0,5')

    #test course with no needed prev knowledge stored
    def test_user_request_needed_knowledge_none(self):
        query = 'What required previous knowledge is there in FE8111?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'No information about required previous knowledge in FE8111 Molecular Beam Epitaxy')


    #test for course with recommended prev knowledge
    def test_user_request_recommended_knowledge(self):
        query = 'What recommended previous knowledge is there in TDT4140?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'Recommended previous knowledge for TDT4140 Software Engineering is: Subjects TDT4100 Object-Oriented Programming and TDT4120 Algorithms and Data Structures, or equivalent.')

    #test for course with no recommended prev knowledge
    def test_user_request_recommended_knowledge_none(self):
        query = 'What recommended previous knowledge is there in EXPH0004?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output, 'No information about recommended previous knowledge for EXPH0004 Examen philosophicum for Science and Technology')


    def test_user_request_not_valid_coursecode(self):
        query = 'Who is the teacher in TYU7643?'
        response = self.load_text_request_with_query(query)
        output = user_request(response)
        self.assertEqual(output,'No course with code TYU7643')

#tests for ask_apiai in crowbot_chat

            #skriv coverage run --source='.' manage.py test myapp
#i fil directiory hvor manage.py ligger
#skriv så coverage report for å få prosenter