from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

from .models import Course

# Create your views here.

def index(request):
    return HttpResponse('api index')

def all_courses(request):
    courses = Course.objects.all()
    return HttpResponse(
        serializers.serialize('json', courses)
    )
