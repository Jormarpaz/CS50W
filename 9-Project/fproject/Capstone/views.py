import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse
import os

from .tests.generator import extract_text_from_file, extract_key_phrases, generate_questions
from .models import User, File, Test, Folder
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
def delete_file(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            file_id = data.get("file_id")

            file = File.objects.get(id=file_id)
            file_path = file.file.path  # Ruta del archivo en el sistema

            if os.path.exists(file_path):
                os.remove(file_path)  # Borrar archivo físico

            file.delete()  # Borrar de la base de datos

            return JsonResponse({"success": True})
        except File.DoesNotExist:
            return JsonResponse({"success": False, "error": "Archivo no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

@login_required
def delete_folder(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            folder_id = data.get("folder_id")

            folder = Folder.objects.get(id=folder_id)

            # Eliminar archivos dentro de la carpeta
            files = File.objects.filter(folder=folder)
            for file in files:
                file_path = file.file.path
                if os.path.exists(file_path):
                    os.remove(file_path)
                file.delete()

            # Eliminar subcarpetas primero
            Folder.objects.filter(parent=folder).delete()

            folder.delete()  # Finalmente, eliminar la carpeta

            return JsonResponse({"success": True})
        except Folder.DoesNotExist:
            return JsonResponse({"success": False, "error": "Carpeta no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

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
def files(request):
    folders = Folder.objects.filter(user=request.user)
    user_files = File.objects.filter(
        user=request.user, folder__isnull=True).order_by("-date")
    folder_files = {folder.id: File.objects.filter(folder=folder) for folder in folders}
    return render(request, "Capstone/files.html", {
        "folders": folders,
        "user_files": user_files,
        "folder_files": folder_files
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
# ************************ Tests ******************************
# *************************************************************
# *************************************************************
@login_required
def select_file_for_test(request):
    user_files = File.objects.filter(user=request.user)  # Archivos del usuario autenticado
    return render(request, "Capstone/tests.html", {"user_files": user_files})

@login_required
def generate_test(request):
    file_id = request.GET.get("file_id")  # Obtener el ID del archivo seleccionado
    num_questions = int(request.GET.get("num_questions", 5))  # Número de preguntas (por defecto 5)

    if not file_id:
        return redirect("tests")  # Si no se seleccionó archivo, redirigir a la selección

    file = get_object_or_404(File, id=file_id, user=request.user)  # Asegurar que el archivo pertenece al usuario
    file_path = file.file.path  # Ruta del archivo
    text = extract_text_from_file(file_path)  # Extraer el texto del archivo

    questions = generate_questions(text, num_questions)  # Generar preguntas

    # Guardar el test en la base de datos
    test = Test.objects.create(user=request.user, file=file, questions=questions)

    return render(request, "Capstone/test.html", {"test": test})


@login_required
def check_answers(request):
    if request.method == "POST":
        test_id = request.POST.get("test_id")
        test = Test.objects.get(id=test_id, user=request.user)
        correct_answers = 0
        correct_answer_texts = []

        for question in test.questions:
            selected_option_id = request.POST.get(f"question_{question['id']}")
            correct_option = next(option for option in question['options'] if option['is_correct'])
            correct_answer_texts.append(correct_option['text'])
            if selected_option_id and int(selected_option_id) == correct_option['id']:
                correct_answers += 1

        return render(request, "Capstone/results.html", {
            "test": test,
            "correct_answers": correct_answers,
            "total_questions": len(test.questions),
            "correct_answer_texts": correct_answer_texts,
        })

    return redirect("index")

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
