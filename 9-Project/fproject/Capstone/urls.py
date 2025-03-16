from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # Gestión de archivos
    path('files/', views.files, name='files'),
    path('files/upload/', views.upload_file, name='file-upload'),
    path('folders/<int:folder_id>/upload-file/', views.upload_file_in_folder, name='upload_file_in_folder'),
    path('delete-file/', views.delete_file, name='delete_file'),
    path('move-file/', views.move_file, name='move_file'),

     # Gestión de carpetas
    path('folders/create/', views.create_folder, name='create_folder'),
    path('folders/<int:folder_id>/create-subfolder/', views.create_subfolder_in_folder, name='create_subfolder_in_folder'),
    path('folders/<int:folder_id>/', views.folder_files, name='folder_files'),
    path('delete-folder/', views.delete_folder, name='delete_folder'),

    # Otras funciones
    path('clock/', views.clock, name='clock'),
    path('calendar/', views.calendar, name='calendar'),
    path('contact/', views.contact, name='contact'),
]