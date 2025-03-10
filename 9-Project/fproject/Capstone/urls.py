from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('files/', views.files, name='files'),
    path('files/upload/', views.upload_file, name='file-upload'),
    path('files/upload/<int:folder_id>/', views.upload_file, name='file-upload-folder'),
    path('delete-file/', views.delete_file, name='delete_file'),
    path('move-file/', views.move_file, name='move_file'),

    path('folders/create/', views.create_folder, name='create_folder'),
    path('folders/<int:folder_id>/', views.folder_files, name='folder_files'),
    path('delete-folder/', views.delete_folder, name='delete_folder'),

    path('calendar/', views.calendar, name='calendar'),

    path('contact/', views.contact, name='contact'),
]