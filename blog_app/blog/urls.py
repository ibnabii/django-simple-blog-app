from django.contrib.auth.models import User
from django.urls import path
from django.views.generic import ListView, DetailView

from .models import Entry
from . import views

app_name = 'blog'
urlpatterns = [
    path('',
        ListView.as_view(
            model=Entry,
            template_name='home.html'
        ),
        name='home'),
    path('registration/', views.RegistrationView.as_view(), name='register'),
    path('authors/',
         ListView.as_view(
            model=User,
            template_name='authors.html'
         ),
        name='authors'),
    path('entry/create/', views.NewEntryView.as_view(), name='entry-create'),
    path('entry/<int:pk>/',
         DetailView.as_view(
             model=Entry
         ),
         name='entry-details'),
    path('entry/<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry-edit'),
    path('entry/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry-delete'),
    path('entry/mine/', views.OwnedEntriesView.as_view(), name='entry-owned'),
    path('authors/<int:pk>/', views.AuthorsEntriesView.as_view(), name='entry-author'),
]

