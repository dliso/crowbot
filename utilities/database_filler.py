import requests
import json

#base for IME API
base_url = "http://www.ime.ntnu.no/api/course/en/"


#fetch all course codes
def list_of_codes(base_url):
    #base_url = "http://www.ime.ntnu.no/api/course/en/"
    #code = input("Please provide a course code: ")
    courses = requests.get(base_url+'-').json()
    codes = []
    for i in range (len(courses['course'])):
        code = courses['course'][i]['code']
        codes.append(code)
    return codes


#function for name
def get_name(course):
    try:
        name = course["course"]["name"]
        return name
    except:
        return ""



#function for recommended_previous_knowledge
def get_recommended_prev_know(course):
    try:
        for i in range(len(course["course"]["infoType"])):
            if course["course"]["infoType"][i]["code"] == "ANBFORK":
                recommended_previous_knowledge = course["course"]["infoType"][i]["text"]
                return recommended_previous_knowledge
    except:
        return ""



# function for required_previous_knowledge
def get_required_prev_know(course):
    try:
        for i in range(len(course["course"]["infoType"])):
            if course["course"]["infoType"][i]["code"] == "FORK":
                required_previous_knowledge = course["course"]["infoType"][i]["text"]
                return required_previous_knowledge
    except:
        return ""



# function for exam_date
def get_exam_date(course):
    try:
        exam_date = course["course"]["assessment"][0]["date"]
        return exam_date
    except:
        return ""


# function for exam_support_code
def get_exam_support_code(course):
    try:
        exam_support_code = course["course"]["assessment"][0]["examinationSupport"][0]["code"]
        return exam_support_code
    except:
        return ""


# function for exam_support_name
def get_exam_support_name(course):
    try:
        exam_support_name = course["course"]["assessment"][0]["examinationSupport"][0]["name"]
        return exam_support_name
    except:
        return ""


# function for location
def get_location(course):
    try:
        location = course["course"]["location"]
        return location
    except:
        return ""


# function for semester
def get_semester(course):
    try:
        if course["course"]["taughtInSpring"] and course["course"]["taughtInAutumn"]:
            semester = 'Autumn and Spring'
            return semester
        elif course["course"]["taughtInSpring"]:
            semester = 'Spring'
            return semester
        elif course["course"]["taughtInAutumn"]:
            semester = 'Autumn'
            return semester
    except:
        return ""



