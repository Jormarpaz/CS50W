from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('upload', views.upload_file, name='upload'),
    path('files', views.files, name='files'),
    path('calendar', views.calendar, name='calendar'),
    path('contact', views.contact, name='contact'),
    path('tests', views.tests, name='tests'),
]