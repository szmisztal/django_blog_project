from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["title", "text"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 64)
    password = forms.CharField(max_length = 64, widget = forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(max_length = 30, required = False)
    last_name = forms.CharField(max_length = 30, required = False)
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
