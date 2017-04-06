from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import UserQuery as UQ
from django import forms
from account_system.forms import SignUpForm
from account_system.views import signup
from django.contrib.auth import logout

from django.shortcuts import redirect

# Create your views here.



def index(request):
    queries = UQ.objects.all()
    signup(request)
    return render(request, 'frontend/index.html', {'queries': queries})

def new_post(request):
    return render(request, 'frontend/new_post.html', {})

def submit(request):
    uq = UQ(query_text=request.POST['user_query'])
    uq.save()
    return HttpResponseRedirect(reverse('frontend:new_post'))

def profilside(request):
    return render(request, 'frontend/profilside.html')

def logout_view(request):
    logout(request)
    return render(request, 'frontend/profilside.html')

