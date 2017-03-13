from django.conf.urls import url

from . import views

from api import views as api_views

app_name = 'backend'

urlpatterns = [
    url(r'^all_courses/?', views.all_courses, name='all_courses'),
    url(r'^add_course', api_views.add_course, name='add_course'),
    url(r'^ask_question', api_views.respond_to_message, name='ask_question'),
    url(r'^question_queue/(.*)', api_views.questions_for_course, name='question_queue'),
    url(r'', views.index, name='index'),
]
