import json

from django.utils import timezone as tz
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from backend.models import Course

# Create your views here.

@csrf_exempt
def add_course(request):
    if request.method == 'POST':
        print(request.body.decode())
        # The deserializer needs to know which model to use. We wrap the req.
        # body in the necessary JSON here.
        wrapped = '[{"model": "backend.course", "fields": %s}]' % request.body.decode()
        for d in serializers.deserialize('json', wrapped):
            d.save()
        return HttpResponse('Added %s to the database.' % d.object.code)
    else:
        return HttpResponse('Send POST requests here to add courses to the database.')
