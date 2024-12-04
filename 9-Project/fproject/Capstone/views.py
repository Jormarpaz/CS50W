from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse


from .models import User, File
from .forms import FileUploadForm

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_files = File.objects.filter(user = request.user).order_by("-uploaded_at")[:5]
        return render(request, "Capstone/index.html", {
            "files": user_files,
        })

@login_required
def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            return redirect("index")
        else:
            form = FileUploadForm()
        return render(request, "Capstone/upload.html", {"form": form})






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
