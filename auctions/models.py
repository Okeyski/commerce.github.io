from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=65)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    name = models.CharField(max_length=65)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    placed_bid = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    image = models.ImageField(upload_to="auction_images", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)
    watchlist = models.ManyToManyField(User, related_name='watchlist_items', blank=True)

    def __str__(self):
        return self.name

class Bid(models.Model):    
    item = models.CharField(max_length=65)    
    price = models.DecimalField(max_digits=6, decimal_places=2)
    placed_by = models.ForeignKey(User, related_name='bid_placed', on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    product = models.ForeignKey(AuctionListing, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)  
    created_by = models.ForeignKey(User, related_name='comments_made', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
