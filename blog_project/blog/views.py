from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import generic
from .forms import RegisterForm, LoginForm
from django.contrib import messages


class HomepageView(generic.TemplateView):
    template_name = "homepage.html"


def sign_up(request):
    template_name = "register.html"
    if request.method == "GET":
        form = RegisterForm()
        return render(request, template_name, {"form": form})
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            user.set_group()
            messages.success(request, "Registration success, you can log in now.")
            return redirect("login")
        else:
            return render(request, template_name, {"form": form})

def sign_in(request):
    template_name = "login.html"
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username = username, password = password)
            if user:
                login(request, user)
                messages.success(request, "You're logged in.")
                return redirect("homepage")
        messages.error(request, "Wrong username or password.")
    else:
        if request.user.is_authenticated:
            return redirect("homepage")
        form = LoginForm()
    return render(request, template_name, {"form": form})

def sign_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")
