from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import RegisterForm, LoginForm, EntryForm
from .models import Entry


# ENTRIES VIEWS:

class HomepageView(generic.TemplateView):
    template_name = "homepage.html"

@method_decorator(login_required, name = "dispatch")
class EntryDetailView(DetailView):
    model = Entry
    context_object_name = "entry_detail"
    template_name = "entry_detail.html"

@method_decorator(login_required, name = "dispatch")
class EntryListView(ListView):
    model = Entry
    paginate_by = 25
    context_object_name = "entries_list"
    template_name = "entries_list.html"

    def get_queryset(self):
        return Entry.objects.order_by("author", "publication_date")

@method_decorator(login_required, name = "dispatch")
class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "entry_form.html"
    success_url = "/blog/entries_list/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Entry was created successfully")
        return response

@method_decorator(login_required, name = "dispatch")
class EntryUpdateView(UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "entry_form.html"

    def get_success_url(self):
        return reverse_lazy("entry_detail", kwargs = {"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Entry was edited successfully")
        return response

@method_decorator(login_required, name = "dispatch")
class EntryDeleteView(DeleteView):
    model = Entry
    template_name = "entry_delete.html"
    success_url = "/blog/entries_list/"

    def get_success_url(self):
        return reverse_lazy("entries_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Entry was deleted successfully")
        return response


# USER SERVICE FUNCTIONS:

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
