from django.core.management.base import BaseCommand, CommandError

from backend.models import Course, Question, Answer
from backend.lemmalize import lemmalize
import pickle

class Command(BaseCommand):
    help = 'Fills the database with often asked questions for all courses.'

    def handle(self, *args, **options):
        # feel free til å forbedre formuleringen til sprøsmålene og legge til flere (husk da å legge til i listen
        # list_of_questions)!
        q1 = 'How many exercises need to be approved?'
        q2 = 'If I have completed the exercises previously, do I have to redo them?'
        q3 = 'How many exercises are there in total?'
        q4 = 'How many exercises do I need to compete to get access the exam?'
        q5 = 'Which textbook is used?'
        q6 = 'Where and when is the first lecture?'
        q7 = 'What is the course homepage?'
        list_of_questions = [q1, q2, q3, q4, q5, q6, q7]
        dict_q_and_lemmas = {}
        for question in list_of_questions:
            dict_q_and_lemmas[question] = lemmalize(question)

        for course in Course.objects.all():
            print(course.code.lower())
            for entry in dict_q_and_lemmas:
                keywords = dict_q_and_lemmas[entry]
                keywords.append(course.code.lower())
                keywords_pickled = pickle.dumps(keywords)
                Question.objects.create(course = course, text = entry, lemma = keywords_pickled)


