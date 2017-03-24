from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


app_name = 'frontend'

urlpatterns = [
    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^profilside/$', views.profilside, name='profilside'),
]
