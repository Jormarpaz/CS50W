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
    path('folders/create/', views.create_folder, name='create_folder'),
    path('folders/<int:folder_id>/', views.folder_files, name='folder_files'),

    path('borrar_archivo/',views.delete_file, name='delete_file'),
    path('borrar_carpeta/',views.delete_folder, name='delete_folder'),

    path('calendar/', views.calendar, name='calendar'),

    path('contact/', views.contact, name='contact'),

    path('tests/', views.select_file_for_test, name='tests'),
    path('generate-test/', views.generate_test, name='generate-test'),
    path('check_answers/', views.check_answers, name='check_answers'),
]