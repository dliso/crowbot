from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views as core_views


urlpatterns = [
    url(r'^$|^profile/$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'frontend:index'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
]
