from django.conf.urls import url

from . import views

from api import views as api_views

app_name = 'backend'

urlpatterns = [
    url(r'^all_courses/?', views.all_courses, name='all_courses'),
    url(r'^add_course', api_views.add_course, name='add_course'),
    url(r'', views.index, name='index'),
]
