from django.conf.urls import url

from . import views

from api import views as api_views

app_name = 'backend'

urlpatterns = [
    url(r'^all_courses/?$', views.all_courses, name='all_courses'),
    url(r'^courses/(.*)/?$', api_views.courses_matching, name='courses_matching'),
    url(r'^all_questions/?$', views.all_questions, name='all_questions'),
    url(r'^add_course/?$', api_views.add_course, name='add_course'),
    url(r'^ask_question/?$', api_views.respond_to_message, name='ask_question'),
    url(r'^answers_for/(.*)/?$', api_views.answers_for_question, name='ask_question'),
    url(r'^submit_answer/?$', api_views.submit_answer, name='submit_answer'),
    url(r'^my_courses/?$', api_views.my_courses, name='my_courses'),
    url(r'^subscribe_to/(.*)/?$', api_views.subscribe_to_course, name='subscribe_to_course'),
    url(r'^unsubscribe_from/(.*)/?$', api_views.unsubscribe_from_course, name='unsubscribe_from_course'),
    url(r'^toggle_interest/?$', api_views.plus_one_question, name='toggle_interest'),
    url(r'^vote_answer/?$', api_views.vote_on_answer, name='vote_answer'),
    url(r'^unsubscribe_from/(.*)/?$', api_views.unsubscribe_from_course, name='unsubscribe_from_course'),
    url(r'^my_feed/?$', api_views.user_feed, name='my_feed'),
    url(r'^chat_log/?$', api_views.chat_log, name='chat_log'),
    url(r'^question_queue/(.*)/?$', api_views.questions_for_course, name='question_queue'),
    url(r'^$', views.index, name='index'),
]
