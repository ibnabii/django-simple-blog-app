from django.urls import path

from . import views


app_name = 'hredirect'
urlpatterns = [
    path('<str:secrethash>/', views.hash_redirect, name='first'),
    path('<str:secrethash>/qr/', views.render_qr_code, name='qr_code'),
]