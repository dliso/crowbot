from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import UserQuery as UQ

# Create your views here.

def index(request):
    queries = UQ.objects.all()
    return render(request, 'frontend/index.html', {'queries': queries})

def new_post(request):
    return render(request, 'frontend/new_post.html', {})

def submit(request):
    uq = UQ(query_text=request.POST['user_query'])
    uq.save()
    return HttpResponseRedirect(reverse('frontend:new_post'))
