from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:pk>", views.listing_view, name="listing"),
    path("<int:pk>/add-watchlist", views.add_watchlist, name="add_watchlist"),
    path("<int:pk>/remove-watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("<int:pk>/watchlist", views.watchlist_view, name="watchlist"),
    path("<int:pk>/newBid", views.newBid, name="newBid"),
    path("<int:pk>/comment", views.comment, name="comment"),
    path("<int:pk>/closeAuction", views.close_auction, name="closeAuction"),
    path("closed", views.closed, name="closed"),
    path("categories", views.categories, name="categories"),
    path("<int:pk>/category-view", views.category_view, name="category_view"),
    path("new", views.new, name="new")
]
