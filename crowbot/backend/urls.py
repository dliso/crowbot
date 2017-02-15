from django.conf.urls import url

from . import views

app_name = 'backend'

urlpatterns = [
    url(r'^all_courses/?', views.all_courses, name='all_courses'),
    url(r'', views.index, name='index'),
]
