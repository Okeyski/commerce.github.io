from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect 
from django.urls import reverse
from .forms import NewBidForm, NewListingForm, NewCommentForm
from .models import User, AuctionListing, Category, Bid, Comment


def index(request):
    listings = AuctionListing.objects.filter(is_sold=False)    
     
    return render(request, "auctions/index.html", {
        'listings': listings,
        'categories': categories
    })

def categories(request):
    categories = Category.objects.all()
    listings = AuctionListing.objects.filter(is_sold=False)
    return render(request, "auctions/categories.html", {
        'categories': categories,
        'listings': listings
    })

def category_view(request, pk):
    category_id = Category.objects.get(pk=pk)
    listings = AuctionListing.objects.filter(is_sold=False, category_id=category_id)
    return render(request, "auctions/category-listing.html", {
        'listings': listings
    })

@login_required(login_url='/login')
def new(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.save()
            return redirect('listing', pk=listing.id)
        
    else:
        form = NewListingForm()
        return render(request, 'auctions/new.html',{
        'form': form
    })

@login_required(login_url='/login')
def closed(request):
    listings = AuctionListing.objects.filter(is_sold=True)
    bids = Bid.objects.filter(placed_by = request.user)
    #category_id = AuctionListing.objects.get(=pk)
    return render(request, "auctions/closed.html", {
        'listings': listings,
        'bids': bids
    })

@login_required(login_url='/login')
def listing_view(request, pk):
    form = NewBidForm()
    comment_form = NewCommentForm()
    listing = get_object_or_404(AuctionListing, pk=pk)
    comments = Comment.objects.filter(product=listing)
    #bid = get_object_or_404(Bid, pk=pk)
    return render(request, 'auctions/listing.html',{
        'listing': listing,
        'form': form,
        'comment_form': comment_form,
        'comments': comments
    })

@login_required(login_url='/login')
def add_watchlist(request, pk):
    item = get_object_or_404(AuctionListing, pk=pk)
    item.watchlist.add(request.user)
    return redirect('listing', pk=item.id)

@login_required
def remove_watchlist(request, pk):
    item = get_object_or_404(AuctionListing, pk=pk)
    item.watchlist.remove(request.user)
    return redirect('listing', pk=item.id)  
  
@login_required(login_url='/login')
def watchlist_view(request, pk):
    watchlist = request.user.watchlist_items.all()
    return render(request, 'auctions/watchlist.html',{
        'watchlist': watchlist 
    })

@login_required(login_url='/login')
def newBid(request, pk):
    if request.method == 'POST':
        form = NewBidForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data["price"]
            print(price)
            listing = get_object_or_404(AuctionListing, pk=pk)
            if price > listing.price and price > listing.placed_bid:
                listing.placed_bid = price
                listing.save()
                bid_update = Bid(item=listing.name, placed_by=request.user, price=listing.placed_bid)
                bid_update.save() 
                return render(request, 'auctions/listing.html',{
        'listing': listing,
        'message': 'Bid lodged successfully',
        'updated': True,
        'form': NewBidForm()
    }) 
            #redirect('listing', pk=item.id)  
            else:
                return render(request, "auctions/listing.html", {
                    'listing': listing,
                    'message': 'Bid lower than the price or current bid!',
                    'updated': False,
                    'form': NewBidForm()
                    })
    return render(request, 'auctions/listing.html',{
        'listing': listing,
        'form': NewBidForm()  
    })

@login_required(login_url='/login')            
def close_auction(request, pk):
    listing = get_object_or_404(AuctionListing, pk=pk)
    listing.is_sold = True
    listing.save()
    return redirect('index')

@login_required(login_url='/login')
def comment(request, pk):
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            listing = AuctionListing.objects.get(pk=pk)
            comment_update = Comment(product=listing, content=content, created_by=request.user)
            comment_update.save()
            return redirect('listing', pk=listing.id)
    return redirect('index')


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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
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
