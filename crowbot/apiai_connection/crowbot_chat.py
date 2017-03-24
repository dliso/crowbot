
from django.conf import settings
#settings.configure()
import sys, json, codecs, apiai, re, pickle
import requests
import django
django.setup()
from backend.models import Course, Question, Answer
from backend.jaccard_similarity import *
from backend.lemmalize import *
from django.core import serializers




json_dump = lambda data: json.dumps(data, cls=serializers.json.DjangoJSONEncoder)

CLIENT_ACCESS_TOKEN = '1b0f421f4b1045c5a9b29c8372573383'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

def crowbot_answer(response):
    return(response["result"]["fulfillment"]["speech"])



def user_request(response):
    #response is a dict
    #what course are the user interested in
    code = response["result"]["parameters"]["course"].upper()


    #find what action to perform
    action = response["result"]["action"]

    #ime api
    #base_url = "http://www.ime.ntnu.no/api/course/en/"

    #go trough every course code to find a match
    try:
        #get the object that contains the right subject
        course = Course.objects.get(code=code)

        #get the name of the course code
        name = course.name

        # find the action of the question and to a specific task based on that
        if action == 'find_credit':
            return(credit(course, response, code, name))
        elif action == 'find_exam_date':
            return(exam_date(course, response, code, name))
        elif action == 'find_location':
            return(location(course, response, code, name))
        elif action == 'find_lecturer_name':
            return(professor_name(course, response, code, name))
        elif action == 'find_email_address':
            return(professor_mail(course, response, code, name))
        elif action == 'find_semester':
            return(semester_taught(course, response, code, name))
        elif action == 'find_aids':
            return(exam_aids(course, response, code, name))
        elif action == 'find_needed_previous_knowledge':
            return(needed_previous_knowledge(course, response, code, name))
        elif action == 'find_recommended_previous_knowledge':
            return(recommended_previous_knowledge(course, response, code, name))
    except django.core.exceptions.ObjectDoesNotExist:
    #if no code matches
        return("No course with code {:s}.".format(code))

    #just test prints
    # print("Course:",code)
    # print("Recognized action:", response["result"]["action"])
    # print()


#FUNCTIONS FOR DIFFERENT ACTIONS

#function for credit
#må muligens endre litt på denne for å få ut tallet i bra format, nei trenger ikke
def credit(course, response, code, name):
    # Crowbot response
    # print(response["result"]["fulfillment"]["speech"])
    # real response
    credit = course.ects_credits
    if credit == None:
        return('No information about credits in this course, {:s} {:s}.'.format(code, name))
    return("Credits for {:s} {:s} is {:s}.".format(code, name, str(credit)))


#function for exam date
#må muligens endre litt på denne for å få ut datoen i bra format, OK I think now
def exam_date(course, response, code, name):
    exam_date = course.exam_date
    if exam_date == None:
        return("No info about the exam in this course {:s} {:s}.".format(code, name))
    # Crowbot response
    # print(response["result"]["fulfillment"]["speech"])
    # real response
    return("Exam date for {:s} {:s} is {:s}.".format(code, name, exam_date.strftime('%d/%m/%Y')))


#function for location
def location(course, response, code, name):
    location = course.location
    # Crowbot response
    # print(response["result"]["fulfillment"]["speech"])
    # real response
    if not location:
        return("No location information for {:s} {:s}.".format(code, name))
    return("{:s} {:s} is taught in {:s}.".format(code, name, location))



#function for professor name
def professor_name(course, response, code, name):
    teacher_name = course.teacher_name
    # crowbot response
    # print(response["result"]["fulfillment"]["speech"])
    # real response
    if not teacher_name:
        return('No information about the lecturer in {:s} {:s}.'.format(code, name))
    return("{:s} {:s} is taught by {:s}.".format(code, name, teacher_name))


#function for professor email
def professor_mail(course, response, code, name):
    teacher_name = course.teacher_name
    teacher_mail = course.teacher_email
    # Crowbot response
    # print(response["result"]["fulfillment"]["speech"])
    # real response
    if not teacher_name:
        if not teacher_mail:
            return('No information about the professors email in {:s} {:s}.'.format(code, name))
        return ('You can reach the professor in {:s} {:s} at {:s}.'.format(code, name, teacher_mail))
    if not teacher_mail:
        return ("No information about {:s}'s email in {:s} {:s}.".format(teacher_name,code, name))
    return("{:s} {:s} is taught by {:s}. They can be reached at {:s}."
           .format(code, name, teacher_name, teacher_mail))


#function for spring or autumn semester
def semester_taught(course, response, code, name):
    semester = course.semester
    # Crowbot response
    # print(response["result"]["fulfillment"]["speech"])
    # real response
    if not semester:
        return("No information about semesters in {:s} {:s}.".format(code, name))
    return("{:s} {:s} is taught in the {:s}.".format(code, name, semester))


#function for exam aids, code and text
def exam_aids(course, response, code, name):
    exam_support_code = course.exam_support_code
    exam_support_name = course.exam_support_name
    # Crowbot response
    # print(response["result"]["fulfillment"]["speech"])
    # real response
    if not exam_support_code:
        if not exam_support_name:
            return("No information about examination support in {:s} {:s}.".format(code, name))
        return ('Examination support materials for {:s} {:s} is: {:s}'.format(code, name, exam_support_name))
    if not exam_support_name:
        return ('Examination support materials for {:s} {:s} is code {:s}.'.format(code, name, exam_support_code))
    return("Exam support materials for {:s} {:s} is code {:s}: {:s}"
           .format(code, name, exam_support_code, exam_support_name))


#function to find needed previous knowledge
def needed_previous_knowledge(course, response, code, name):
    required_previous_knowledge = course.required_previous_knowledge
    # Crowbot response
    # print(response["result"]["fulfillment"]["speech"])
    # real response
    if not required_previous_knowledge:
        return('No information about required previous knowledge in {:s} {:s}.'.format(code, name))
    return("Required previous knowledge is: {:s}".format(required_previous_knowledge))


# function to find recommended previous knowledge
def recommended_previous_knowledge(course, response, code, name):
    recommended_previous_knowledge = course.recommended_previous_knowledge
    # Crowbot response
    # print(response["result"]["fulfillment"]["speech"])
    # real response
    if not recommended_previous_knowledge:
        return("No information about recommended previous knowledge for {:s} {:s}.".format(code, name))
    return("Recommended previous knowledge for {:s} {:s} is: {:s}"
           .format(code, name, recommended_previous_knowledge))


def ask_apiai(text):
    request = ai.text_request()
    request.query = text
    response = request.getresponse().read().decode()
    response = json.loads(response)
    # print(response)
    if response["result"]["metadata"]["intentName"] == 'Default Welcome Intent':
        return crowbot_answer(response)
    elif response["result"]["metadata"]["intentName"] == 'Default Goodbye Intent':
        return crowbot_answer(response)
    elif response["result"]["metadata"]["intentName"] == "Default Fallback Intent":
        #legge til spørsmål i Questions modell
        question = response["result"]["resolvedQuery"]
        words = re.compile('\w+').findall(question)
        code = ''
        for word in words:
            # antagelse om at alle emnekoder begynner med bokstaver og slutter med tall
            # og at bruker bare skriver inn en emnekode i hver "spørring"
            if re.search('[ÆæØøÅåa-zA-Z]'+'[0-9]', word):
                code = word.upper()
                break
        try:
            course = Course.objects.get(code=code)
            highest_ratio = 0
            similar_question = ''
            similar_question_object = None
            lemmas1 = lemmalize(question)
            lemmas_pickled = pickle.dumps(lemmas1)
            for q in Question.objects.all():
                #ta inn lemma fra question
                lemmas2 = pickle.loads(q.lemma)
                result = jaccard_similarity(lemmas1,lemmas2)
                if result[0]:
                    if result[1]>highest_ratio:
                        highest_ratio = result[1]
                        similar_question_object = q
                        similar_question = q.text
            if similar_question == '':
                Question.objects.create(text=question, course=course, lemma=lemmas_pickled)
                #print(Question.objects.all())
                text_response = 'No similar question detected, your question has been saved for the instructor to answer.'
                return text_response
            else:
                info_list = []
                if similar_question_object.user_id == None:
                    usertype = ''
                    username = ''
                else:
                    usertype = similar_question_object.user_id.role
                    username = similar_question_object.user_id.user.username
                body = similar_question
                timestamp = similar_question_object.creation_datetime
                similar_question_dict = {'usertype': usertype,
                                         'username': username,
                                         'body': body,
                                         'timestamp': timestamp}
                info_list.append(similar_question_dict)
                pk = similar_question_object.pk
                for answer in Answer.objects.filter(question__exact=pk):
                    if answer.user_id == None:
                        usertype = ''
                        username = ''
                    else:
                        usertype = answer.user_id.role
                        username = answer.user_id.user.username
                    body = answer.text
                    timestamp = answer.creation_datetime
                    answer_dict = {'usertype': usertype,
                                   'username': username,
                                   'body': body,
                                   'timestamp': timestamp}
                    info_list.append(answer_dict)
                return info_list



        except django.core.exceptions.ObjectDoesNotExist:
            return crowbot_answer(response)

    elif response["result"]["metadata"]["intentName"] == "Default Help Intent":
        return crowbot_answer(response)
    else:
        return user_request(response)
