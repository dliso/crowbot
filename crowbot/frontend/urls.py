from django.conf.urls import url

from . import views

app_name = 'frontend'

urlpatterns = [
    url(r'^new_post/', views.new_post, name='new_post'),
    url(r'^submit/', views.submit, name='submit'),
    url(r'^$', views.index, name='index'),
]
