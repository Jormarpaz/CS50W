import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import os

from .models import User, File, Folder, Event
from . import forms


def index(request):
    if request.user.is_authenticated:
        user_files = File.objects.filter(
            user=request.user).order_by("-date")[:4]
        now = timezone.now()
        upcoming_events = Event.objects.filter(
            user=request.user, start__gte=now).order_by('start')[:4] 
        return render(request, "Capstone/index.html", {
            "user_files": user_files,
            "upcoming_events": upcoming_events,
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
def upload_file_in_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    if request.method == 'POST':
        form = forms.UploadFileInFolderForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.folder = folder
            file.save()
            return redirect("folder_files", folder_id=folder.id)
    else:
        form = forms.UploadFileInFolderForm()

    return render(request, "Capstone/upload_file_in_folder.html", {
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
    folder_files = {folder.id: File.objects.filter(
        folder=folder) for folder in Folder.objects.filter(user=request.user)}
    return render(request, "Capstone/files.html", {
        "folders": folders,
        "user_files": user_files,
        "folder_files": folder_files,
        "subfolders": subfolders
    })


@login_required
def folder_files(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    subfolders = Folder.objects.filter(user=request.user, parent=folder)
    files = File.objects.filter(user=request.user, folder=folder)
    return render(request, "Capstone/folder_files.html", {"folder": folder, "subfolders": subfolders, "files": files})


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
def create_subfolder_in_folder(request, folder_id):
    parent = get_object_or_404(Folder, id=folder_id, user=request.user)

    if request.method == "POST":
        form = forms.CreateSubfolderForm(request.POST)
        if form.is_valid():
            subfolder = form.save(commit=False)
            subfolder.user = request.user
            subfolder.parent = parent
            subfolder.save()
            return redirect("folder_files", folder_id=parent.id)
    else:
        form = forms.CreateSubfolderForm()
    return render(request, "Capstone/create_subfolder_in_folder.html", {
        "form": form,
        "folder": parent,
    })


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
# ********************** Cronómetro ***************************
# *************************************************************
# *************************************************************


@login_required
def clock(request):
    return render(request, "Capstone/clock.html")

# *************************************************************
# *************************************************************
# ********************** Calendario ***************************
# *************************************************************
# *************************************************************


@csrf_exempt
@login_required
def calendar(request):
    if request.method == 'POST':
        try:
            # Leer los datos JSON enviados
            data = json.loads(request.body)
            print("Datos recibidos:", data)

            # Si es "todo el día", ajustar los campos start y end
            if data.get("allDay", False):
                data["start"] = data.get("start")  
                data["end"] = None  

            # Crear el formulario con los datos recibidos
            form = forms.EventForm(data)
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user  
                event.save()
                return JsonResponse({"success": True})
            else:
                # Si el formulario no es válido, devolver los errores
                print("Errores del formulario:", form.errors)
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
        except Exception as e:
            # Manejar cualquier excepción
            print("Error en la vista calendar:", e)
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    # Si la solicitud no es POST, mostrar el calendario
    user_events = Event.objects.filter(user=request.user).order_by('start')
    events_data = [
        {
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),  # Formato ISO para FullCalendar
            'end': event.end.isoformat() if event.end else None,
            'allDay': event.allDay,
        }
        for event in user_events
    ]

    return render(request, "Capstone/calendar.html", {
        "events_data": json.dumps(events_data), 
        "events": user_events,
    })


@csrf_exempt
@login_required
def delete_event(request, event_id):
    if request.method == 'DELETE':
        try:
            event = Event.objects.get(id=event_id, user=request.user)
            event.delete()
            return JsonResponse({"success": True})
        except Event.DoesNotExist:
            return JsonResponse({"success": False, "error": "Evento no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)


@csrf_exempt
@login_required
def edit_event(request, event_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            event = Event.objects.get(id=event_id, user=request.user)

            event.title = data.get('title', event.title)
            event.start = data.get('start', event.start)
            event.end = data.get('end', event.end)
            event.allDay = data.get('allDay', event.allDay)
            event.save()

            return JsonResponse({"success": True})
        except Event.DoesNotExist:
            return JsonResponse({"success": False, "error": "Evento no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)


# *************************************************************
# *************************************************************
# *********************** Contacto ****************************
# *************************************************************
# *************************************************************

@login_required
def contact(request):
    return render(request, "Capstone/contact.html")


@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Validar que todos los campos estén presentes
            if not all([name, email, subject, message]):
                return JsonResponse({'success': False, 'error': 'Todos los campos son obligatorios.'}, status=400)

            # Enviar el correo electrónico
            send_mail(
                f'Mensaje de contacto: {subject}',
                f'Nombre: {name}\nCorreo: {email}\nMensaje: {message}',
                settings.EMAIL_HOST_USER,  
                [settings.EMAIL_HOST_USER],  
                fail_silently=False,
            )

            # Devolver una respuesta de éxito
            return JsonResponse({'success': True})

        except Exception as e:
            # Manejar cualquier excepción que ocurra durante el proceso
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # Si la solicitud no es POST, devolver un error
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)


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
