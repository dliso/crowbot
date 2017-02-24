# API.AI Example
# This example shows how API.AI can be used to process requests
# The connected bot will recognize requests for news, and will output the requested action and topic
# Feel free to insert your own client access token to connect your own bot
# Author: Audun Liberg

from django.conf import settings
#settings.configure()
import sys, json, codecs, apiai
import requests
import django
django.setup()
from backend.models import Course





CLIENT_ACCESS_TOKEN = '1b0f421f4b1045c5a9b29c8372573383'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

def crowbot_answer(response):
    print(response["result"]["fulfillment"]["speech"])



def user_request(response):

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
        return("No course with code", code)

    #just test prints
    print("Course:",code)
    print("Recognized action:", response["result"]["action"])
    print()


#FUNCTIONS FOR DIFFERENT ACTIONS

#function for credit
#må muligens endre litt på denne for å få ut tallet i bra format, nei trenger ikke
def credit(course, response, code, name):
    try:

        # Crowbot response
        print(response["result"]["fulfillment"]["speech"])
        # real response
        credit = course.ects_credits
        return("Credits for {:s} {:s} is {:s}".format(code, name, str(credit)))
    except:
        print('No information about credits in this course,', code, name)


#function for exam date
#må muligens endre litt på denne for å få ut datoen i bra format, OK I think now
def exam_date(course, response, code, name):
    try:
        exam_date = course.exam_date.strftime('%d/%m/%Y')
        # Crowbot response
        print(response["result"]["fulfillment"]["speech"])
        #real response
        return("Exam date for {:s} {:s} is {:s}".format(code, name, exam_date))
    except:
        print("No info about the exam in this course", code, name)

#function for location
def location(course, response, code, name):
    try:
        location = course.location
        # Crowbot response
        print(response["result"]["fulfillment"]["speech"])
        # real response
        return("{:s} {:s} is taught in {:s}".format(code, name, location))
    except:
        print("No location information for ", code, name)


#function for professor name
def professor_name(course, response, code, name):
    try:
        teacher_name = course.teacher_name
        #crowbot response
        print(response["result"]["fulfillment"]["speech"])
        # real response
        return("{:s} {:s} is taught by {:s}".format(code, name, teacher_name))
    except:
        print('No information about the lecturer in this course,', code, name)


#function for professor email
def professor_mail(course, response, code, name):
    try:
        teacher_name = course.teacher_name
        teacher_mail = course.teacher_email
        # Crowbot response
        print(response["result"]["fulfillment"]["speech"])
        # real response
        return("{:s} {:s} is taught by {:s}. They can be reached at {:s}"
               .format(code, name, teacher_name, teacher_mail))
    except:
        print('No information about the professors email in this course,', code, name)


#function for spring or autumn semester
def semester_taught(course, response, code, name):
    try:
        semester = course.semester
        # Crowbot response
        print(response["result"]["fulfillment"]["speech"])
        # real response
        return("{:s} {:s} is taught in the {:s}".format(code, name, semester))
    except:
        print("No information about semesters in", code, name)

#function for exam aids, code and text
def exam_aids(course, response, code, name):
    try:
        exam_support_code = course.exam_support_code
        exam_support_name = course.exam_support_name
        # Crowbot response
        print(response["result"]["fulfillment"]["speech"])
        # real response
        return("Exam support materials for {:s} {:s} is code {:s}: {:s}"
               .format(code, name, exam_support_code, exam_support_name))
    except:
        print("No information about examination support in ", code, name)


#function to find needed previous knowledge
def needed_previous_knowledge(course, response, code, name):
    try:
        required_previous_knowledge = course.required_previous_knowledge
        # Crowbot response
        print(response["result"]["fulfillment"]["speech"])
        # real response
        return("Needed previous knowledge is: {:s}".format(required_previous_knowledge))
    except:
        print('No information about required previous knowledge in this course (', code, name, ")")


# function to find recommended previous knowledge
def recommended_previous_knowledge(course, response, code, name):
    try:
        recommended_previous_knowledge = course.recommended_previous_knowledge
        # Crowbot response
        print(response["result"]["fulfillment"]["speech"])
        # real response
        return("Recommended previous knowledge for {:s} {:s} is {:s}"
               .format(code, name, recommended_previous_knowledge))
        # return("Recommended previous knowledge in", code, name, " is :", recommended_previous_knowledge)
    except:
        print('No information about recommended previous knowledge in this course (', code, name, ")")


def ask_apiai(text):
    request = ai.text_request()
    request.query = text
    response = request.getresponse().read().decode()
    response = json.loads(response)
    print(response)
    return user_request(response)

#main function
if __name__ == '__main__':

    while True:
        # Create a request
        request = ai.text_request()
        request.query = input("Ask Crowbot something: ")

        # make input uppercase to match the for loop of all course codes
        request.query = request.query.upper()

        # Get respons, convert to json
        response = request.getresponse().read().decode('utf-8')
        response = json.loads(response)

        #what do the user want: geeting/goodbye/dont know/request
        if response["result"]["metadata"]["intentName"] == 'Default Welcome Intent':
            crowbot_answer(response)
        elif response["result"]["metadata"]["intentName"] == 'Default Goodbye Intent':
            crowbot_answer(response)
        elif response["result"]["metadata"]["intentName"] == "Default Fallback Intent":
            crowbot_answer(response)
        elif response["result"]["metadata"]["intentName"] == "Default Help Intent":
            crowbot_answer(response)
        else:
            user_request(response)
        print()
