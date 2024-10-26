from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    return render(request, "network/index.html")

@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        post = Post(user=request.user, content=content)
        post.save()
        return redirect("index")
    return render(request, "network/new_post.html")

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all().order_by("-timestamp")
    followers = user.followers.count()
    following = user.following.count()
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, "network/profile.html", {
        "profile_user": user,
        "posts": posts,
        "followers": followers,
        "following": following,
        "is_following": is_following
    })

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.filter(follower=request.user, following=user_to_follow).delete()
    else:
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect("profile", username=username)

@login_required
def following(request):
    user = request.user
    following_users = user.following.all().values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        content = request.POST["content"]
        post.content = content
        post.save()
        return JsonResponse({"message": "Post updated successfully."}, status=200)
    return JsonResponse({"error": "Invalid request."}, status=400)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if Like.objects.filter(user=request.user, post=post).exists():
        Like.objects.filter(user=request.user, post=post).delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
    return JsonResponse({"liked": liked, "likes_count": post.likes.count()}, status=200)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
