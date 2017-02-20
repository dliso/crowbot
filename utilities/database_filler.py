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