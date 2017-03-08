from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    CHOICES = (('1','Student'),('2','Professor'))
    first_name = forms.CharField(max_length=30, required=True, help_text='*')
    last_name = forms.CharField(max_length=30, required=True, help_text='*')
    email = forms.EmailField(max_length=254, help_text='* Required to cotain @.')
    birth_date = forms.DateField(required=True,help_text=' Format: YYYY-MM-DD')
    roles = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    institute = forms.CharField(max_length=30, required=True, help_text='*')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'roles', 'institute', 'birth_date')

