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