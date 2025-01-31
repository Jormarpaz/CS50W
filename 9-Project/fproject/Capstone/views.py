from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse


from .models import User, File
from . import forms

# Create your views here.
def index(request):
    return render(request, "Capstone/index.html")
    

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
        user=request.user).order_by("date")
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
def tests(request):
    if request.method == "POST":
        test_name = request.POST["test_name"]
        test_description = request.POST["test_description"]
        test_date = request.POST["test_date"]

        # Aquí puedes agregar la lógica para guardar los datos del test en la base de datos
        # o realizar cualquier otra acción necesaria.

        messages.success(request, "Test information has been submitted successfully!")
        return redirect("tests")
    return render(request, "Capstone/tests.html")

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
