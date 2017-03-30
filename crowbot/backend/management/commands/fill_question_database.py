from django.core.management.base import BaseCommand, CommandError

from backend.models import Course, Question, Answer
from backend.lemmalize import lemmalize
import pickle

class Command(BaseCommand):
    help = 'Fills the database with often asked questions for all courses.'

    def handle(self, *args, **options):
        # feel free til å forbedre formuleringen til sprøsmålene og legge til flere (husk da å legge til i listen
        # list_of_questions)!
        # q1 og q3 har samme nøkkelord...
        q1 = 'How many exercises is mandatory'
        q2 = 'If I have completed the exercises in previous years, are they still valid'
        q3 = 'How many exercises are there in total'
        q4 = 'How many exercises do I need to compete to get access the exam'
        q5 = 'Which textbook is used'
        q6 = 'Where and when is the first lecture'
        q7 = 'What is the course homepage'
        list_of_questions = [q1, q2, q3, q4, q5, q6, q7]

        for course in Course.objects.all():
            for question in list_of_questions:
                new_question = question + ' in {:s}?'.format(course.code)
                print(new_question)
                keywords = lemmalize(new_question)
                print(keywords)
                keywords_pickled = pickle.dumps(keywords)
                # Question.objects.create(course = course, text = new_question, lemma = keywords_pickled)


