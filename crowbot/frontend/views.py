from django.shortcuts import render
from django.http import HttpResponse

from .models import UserQuery as UQ

# Create your views here.

def index(request):
    queries = UQ.objects.all()
    return render(request, 'frontend/index.html', {'queries': queries})
