from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm


@login_required
def home(request):
    return HttpResponseRedirect(reverse('frontend:index'))

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.birthdate = form.cleaned_data.get('birth_date')
            user.profile.institute = form.cleaned_data.get('institute')
            user.profile.role = form.cleaned_data.get('roles')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render (request, 'frontend/profilside.html', {'form': form})
