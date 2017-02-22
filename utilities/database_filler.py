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
            else:
                return ""
    except:
        return ""



# function for required_previous_knowledge
def get_required_prev_know(course):
    try:
        for i in range(len(course["course"]["infoType"])):
            if course["course"]["infoType"][i]["code"] == "FORK":
                required_previous_knowledge = course["course"]["infoType"][i]["text"]
                return required_previous_knowledge
            else:
                return ""
    except:
        return ""



# function for exam_date
def get_exam_date(course):
    try:
        for i in range(len(course["course"]["assessment"])):
            try:
                exam_date = course["course"]["assessment"][i]["date"]
                return exam_date
            except KeyError:
                continue
    except:
        return
    return


# function for exam_support_code
def get_exam_support_code(course):
    try:
        for i in range(len(course["course"]["assessment"])):
            try:
                exam_support_code = course["course"]["assessment"][i]["examinationSupport"][0]["code"]
                return exam_support_code
            except KeyError:
                continue
    except:
        return ""
    return ""


# function for exam_support_name
def get_exam_support_name(course):
    try:
        for i in range(len(course["course"]["assessment"])):
            try:
                exam_support_name = course["course"]["assessment"][i]["examinationSupport"][0]["name"]
                return exam_support_name
            except KeyError:
                continue
    except:
        return ""
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
        else:
            return ""
    except:
        return ""


# function for teacher_name
def get_teacher_name(course):
    try:
        teacher_name = course["course"]["educationalRole"][0]["person"]["displayName"]
        return teacher_name
    except:
        return ""



# function for teacher_email
def get_teacher_email(course):
    try:
        teacher_email = course["course"]["educationalRole"][0]["person"]["email"]
        return teacher_email
    except:
        return ""



# function for ects_credit
def get_credit(course):
    try:
        ects_credits = course["course"]["credit"]
        return ects_credits
    except:
        return



def fill_database():
    #go trough every course code to add to database
    #for code in list_of_codes(base_url):
    #code = 'AAR4990'
    code = 'TMA4100'
    # Fetch the course
    course = requests.get(base_url + code).json()
    name = get_name(course)
    recommended_previous_knowledge = get_recommended_prev_know(course)
    required_previous_knowledge = get_required_prev_know(course)
    exam_date = get_exam_date(course)
    exam_support_code = get_exam_support_code(course)
    exam_support_name = get_exam_support_name(course)
    location = get_location(course)
    semester = get_semester(course)
    teacher_name = get_teacher_name(course)
    teacher_email = get_teacher_email(course)
    ects_credits = get_credit(course)
    attributes = {'code':code,'name':name, 'recommended_previous_knowledge':recommended_previous_knowledge,
                                     'required_previous_knowledge':required_previous_knowledge, 'exam_date':exam_date,
                                     'exam_support_code':exam_support_code, 'exam_support_name':exam_support_name,
                                     'location':location, 'semester':semester, 'teacher_name':teacher_name,
                                     'teacher_email':teacher_email, 'ects_credits':ects_credits}
    requests.post('http://localhost:8000/api/add_course',
                  data = json.dumps(attributes))



if __name__ == '__main__':
    fill_database()
    #litt rart i databasen at første emne får pk = 618, og siste pk = 5230, men antallet stemmer
    #da listen over alle koder inneholder 4613 emner


