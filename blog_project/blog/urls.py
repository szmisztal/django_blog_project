from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name = "homepage"),
    path("register/", views.sign_up, name = "register"),
    path("login/", views.sign_in, name = "login"),
    path("logout/", views.sign_out, name = "logout"),
    path("entry/<int:pk>/", views.EntryDetailView.as_view(), name = "entry_detail"),
    path("entries_list/", views.EntryListView.as_view(), name = "entries_list"),
    path("entry_create/", views.EntryCreateView.as_view(), name = "entry_create"),
    path("entry_update/<int:pk>", views.EntryUpdateView.as_view(), name = "entry_update"),
    path("entry_delete/<int:pk>/", views.EntryDeleteView.as_view(), name = "entry_delete")
]
