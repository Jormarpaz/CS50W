from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True)
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = float(request.POST["price"])
        image_url = request.POST["image"]
        category = request.POST["category"]

        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            user=request.user,
            active=True,
        )
        listing.save()
        return redirect("index")
    else:
        return render(request, "auctions/create_listing.html")

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    user = request.user
    is_watchlist = False
    if user.is_authenticated:
        is_watchlist = Watchlist.objects.filter(user=user, listing=listing).exists()

    if request.method == "POST":
        if "bid_amount" in request.POST:
            bid_amount = float(request.POST["bid_amount"])
            if bid_amount >= listing.starting_bid and (listing.current_bid is None or bid_amount > listing.current_bid):
                Bid.objects.create(user=user, listing=listing, bid=bid_amount)
                listing.current_bid = bid_amount
                listing.save()
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "error": "Your bid must be at least as large as the starting bid and greater than any other bids.",
                    "is_watchlist": is_watchlist,
                    "comments": Comment.objects.filter(listing=listing)
                })
        elif "watchlist" in request.POST:
            if is_watchlist:
                Watchlist.objects.filter(user=user, listing=listing).delete()
            else:
                Watchlist.objects.create(user=user, listing=listing)
            is_watchlist = not is_watchlist
        elif "close_auction" in request.POST and listing.user == user:
            listing.active = False
            listing.save()
        elif "comment" in request.POST:
            comment_text = request.POST["comment"]
            Comment.objects.create(user=user, listing=listing, comment=comment_text)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watchlist": is_watchlist,
        "comments": Comment.objects.filter(listing=listing)
    })

def watchlist(request):
    user = request.user
    listings = Listing.objects.filter(watchlist__user=user)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def watchlist_count(request):
    if request.user.is_authenticated:
        count = Watchlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'watchlist_count': count}

def categories(request):
    categories = Listing.objects.filter(active=True).values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_name):
    listings = Listing.objects.filter(category=category_name, active=True)
    return render(request, "auctions/category.html", {
        "category": category_name,
        "listings": listings
    })

def bid(request, listing_id):
    if request.method == "POST":
        pass
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))