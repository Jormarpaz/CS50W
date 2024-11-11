from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Like, Follow, Comment


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })

@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        post = Post(user=request.user, content=content)
        post.save()
        return redirect("index")
    return render(request, "network/new_post.html")

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)  # Limitar a 10 publicaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    followers = user.followers.count()
    following = user.following.count()
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    return render(request, "network/profile.html", {
        "profile_user": user,
        "page_obj": page_obj,
        "followers": followers,
        "following": following,
        "is_following": is_following,
        "liked_posts": liked_posts
    })

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    # Obtener otros datos necesarios para el perfil
    posts = profile_user.posts.all().order_by("-timestamp")
    followers = profile_user.followers.count()
    following = profile_user.following.count()
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following
    }
    return render(request, 'network/profile.html', context)

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.filter(follower=request.user, following=user_to_follow).delete()
        is_following = False
    else:
        Follow.objects.create(follower=request.user, following=user_to_follow)
        is_following = True
    return JsonResponse({"is_following": is_following, "followers": user_to_follow.followers.count()}, status=200)

@login_required
def follow_view(request, username):
    if request.method == "PUT":
        profile_user = get_object_or_404(User, username=username)
        if request.user == profile_user:
            return JsonResponse({"error": "You cannot follow yourself."}, status=400)

        if Follow.objects.filter(user=request.user, following=profile_user).exists():
            Follow.objects.filter(user=request.user, following=profile_user).delete()
            is_following = False
        else:
            Follow.objects.create(user=request.user, following=profile_user)
            is_following = True

        followers_count = profile_user.followers.count()
        return JsonResponse({"is_following": is_following, "followers": followers_count}, status=200)
    return JsonResponse({"error": "PUT request required."}, status=400)

@login_required
def following(request):
    user = request.user
    
    following_users = user.following.all().values_list('following', flat=True)
    
    posts = Post.objects.filter(user__in=following_users).order_by("-timestamp")
   
    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    
    return render(request, "network/following.html", {
        "posts": posts,
        "liked_posts": liked_posts
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
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        if Like.objects.filter(user=request.user, post=post).exists():
            Like.objects.filter(user=request.user, post=post).delete()
            liked = False
        else:
            Like.objects.create(user=request.user, post=post)
            liked = True
        return JsonResponse({"liked": liked, "likes_count": post.likes.count()}, status=200)
    return JsonResponse({"error": "POST request required."}, status=400)

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST["content"]
        if content.strip() == "":
            messages.error(request, "Comment cannot be empty.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        comment = Comment(user=request.user, post=post, content=content)
        comment.save()
        messages.success(request, "Comment added successfully.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    messages.error(request, "POST request required.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
