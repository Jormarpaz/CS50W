from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('files/', views.files, name='files'),
    path('upload/', views.upload_file, name='file-upload'),

    path('calendar/', views.calendar, name='calendar'),

    path('contact/', views.contact, name='contact'),

    path('tests/', views.select_file_for_test, name='tests'),
    path('generate-test/', views.generate_test, name='generate-test'),
]