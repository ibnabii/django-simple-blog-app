from django.urls import path

from . import views


app_name = 'hredirect'
urlpatterns = [
    path('<str:hash>/', views.hash_redirect, name='first'),
]