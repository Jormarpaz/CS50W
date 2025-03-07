import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse
import os

from .models import User, File, Folder
from . import forms

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_files = File.objects.filter(
            user=request.user).order_by("-date")
        return render(request, "Capstone/index.html", {
            "user_files": user_files,
        })
    else:
        return render(request, "Capstone/index.html")
    
# *************************************************************
# *************************************************************
# *********************** Archivos ****************************
# *************************************************************
# *************************************************************

@login_required
def upload_file(request, folder_id=None):
    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    if request.method == 'POST':
        form = forms.UploadFile(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            if folder:
                file.folder = folder
            file.save()
            return redirect("files")
    else:
        form = forms.UploadFile()
    return render(request, "Capstone/upload.html", {
        "form": form,
        "folder": folder,
    })

@login_required
@require_POST
def delete_file(request):
    data = json.loads(request.body)
    file_id = data.get('file_id')
    if not file_id:
        return JsonResponse({'success': False, 'error': 'ID de archivo no proporcionado'}, status=400)

    try:
        file = File.objects.get(id=file_id)
        file_path = file.file.path
        if os.path.exists(file_path):
            os.remove(file_path)
        file.delete()
        return JsonResponse({'success': True})
    except File.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Archivo no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
@login_required
def files(request):
    folders = Folder.objects.filter(user=request.user, parent__isnull=True)
    subfolders = Folder.objects.filter(user=request.user, parent__isnull=False)
    user_files = File.objects.filter(
        user=request.user, folder__isnull=True).order_by("-date")
    folder_files = {folder.id: File.objects.filter(folder=folder) for folder in Folder.objects.filter(user=request.user)}
    return render(request, "Capstone/files.html", {
        "folders": folders,
        "user_files": user_files,
        "folder_files": folder_files,
        "subfolders": subfolders
    })

@login_required
def folder_files(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    files = File.objects.filter(user=request.user, folder=folder)
    return render(request, "Capstone/folder_files.html", {"folder": folder, "files": files})

@login_required
def create_folder(request):
    if request.method == "POST":
        form = forms.FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            return redirect("files")
    else:
        form = forms.FolderForm()
    return render(request, "Capstone/create_folder.html", {"form": form})

@login_required
def delete_folder(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Datos recibidos:", data)
            folder_id = data.get("folder_id")

            if not folder_id:
                return JsonResponse({"success": False, "error": "ID de carpeta no proporcionado"}, status=400)

            folder = Folder.objects.get(id=folder_id)    

            files = File.objects.filter(folder=folder)
            if files.exists():
                for file in files:
                    file_path = file.file.path
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    file.delete()
            
            def delete_subfolders(folder):
                subfolders = Folder.objects.filter(parent=folder)
                for subfolder in subfolders:
                    delete_subfolders(subfolder)
                    subfolder.delete()

            delete_subfolders(folder)

            folder.delete()

            return JsonResponse({"success": True})
        except Folder.DoesNotExist:
            return JsonResponse({"success": False, "error": "Carpeta no encontrada"}, status=404)
        except Exception as e:
            print("Error en delete_folder:", e)
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

# *************************************************************
# *************************************************************
# *********************** Arrastre ****************************
# *************************************************************
# *************************************************************

@login_required
def move_file(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            file_id = data.get("file_id")
            folder_id = data.get("folder_id")

            if not file_id:
                return JsonResponse({"success": False, "error": "ID de archivo no proporcionado"}, status=400)

            file = File.objects.get(id=file_id, user=request.user)
            if folder_id:
                folder = Folder.objects.get(id=folder_id, user=request.user)
                file.folder = folder
            else:
                file.folder = None
            file.save()

            return JsonResponse({"success": True})
        except File.DoesNotExist:
            return JsonResponse({"success": False, "error": "Archivo no encontrado"}, status=404)
        except Folder.DoesNotExist:
            return JsonResponse({"success": False, "error": "Carpeta no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

# *************************************************************
# *************************************************************
# ********************** Calendario ***************************
# *************************************************************
# *************************************************************

@login_required
def calendar(request):
    user_events = File.objects.filter(
        user=request.user).order_by("date")
    return render(request, "Capstone/calendar.html", {
        "events": user_events,
    })

# *************************************************************
# *************************************************************
# *********************** Contacto ****************************
# *************************************************************
# *************************************************************

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]

        # Aquí puedes agregar la lógica para enviar el mensaje por correo electrónico
        # o guardarlo en la base de datos, según tus necesidades.

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")
    return render(request, "Capstone/contact.html")


############################################
############################################
############### AUTENTICACION ##############
############################################
############################################


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "Capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, 'Capstone/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Capstone/register.html")
