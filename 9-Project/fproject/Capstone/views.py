from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse


from .tests.generator import extract_text_from_file, extract_key_phrases, generate_questions
from .models import User, File, Test
from . import forms

# Create your views here.
def index(request):
    user_files = File.objects.filter(
        user=request.user).order_by("-date")
    return render(request, "Capstone/index.html", {
        "user_files": user_files,
    })
    
# *************************************************************
# *************************************************************
# *********************** Archivos ****************************
# *************************************************************
# *************************************************************

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = forms.UploadFile(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            return redirect("files")
    else:
        form = forms.UploadFile()
    return render(request, "Capstone/upload.html", {
        "form": form,
    })
    


@login_required
def files(request):
    user_files = File.objects.filter(
        user=request.user).order_by("-date")
    return render(request, "Capstone/files.html", {
        "user_files": user_files,
    })

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
        return redirect("select-test-file")  # Si no se seleccionó archivo, redirigir a la selección

    file = get_object_or_404(File, id=file_id, user=request.user)  # Asegurar que el archivo pertenece al usuario
    file_path = file.file.path  # Ruta del archivo
    text = extract_text_from_file(file_path)  # Extraer el texto del archivo

    questions = generate_questions(text, num_questions)  # Generar preguntas

    # Guardar el test en la base de datos
    test = Test.objects.create(user=request.user, file=file, questions=questions)

    return render(request, "Capstone/test.html", {"test": test})

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
