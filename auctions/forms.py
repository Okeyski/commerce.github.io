from django import forms
from .models import Bid, AuctionListing

ATTRIBUTE = 'mb-6 w-full py-4 px-6 rounded-xl border'

class NewBidForm(forms.Form):
    price = forms.DecimalField(label="", min_value=1, widget=forms.TextInput(
            attrs={
                "class": "appaerance-none bg-white border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none",
            }
        ))

class NewListingForm(forms.ModelForm):
    class Meta:
         model = AuctionListing
         fields =('name', 'category', 'price', 'image', 'description',) 
         widgets = {
            'name': forms.TextInput(attrs={
                'class': ATTRIBUTE
            }),
            'category': forms.Select(attrs={
                'class': ATTRIBUTE
            }),
            'price': forms.TextInput(attrs={
                'class': ATTRIBUTE
            }),
            'image': forms.FileInput(attrs={
                'class': ATTRIBUTE
            }),
            'description': forms.Textarea(attrs={
                'class': ATTRIBUTE
            }), 
            
         }

class NewCommentForm(forms.Form):
    content = forms.CharField(label="", widget=forms.TextInput(
            attrs={
                "class": "bg-gray-100 rounded border border-gray-400 leading-normal resize-none w-full h-20 py-2 px-3 font-medium placeholder-gray-700 focus:outline-none focus:bg-white",
            }
        ))
