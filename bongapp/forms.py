from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import TextInput,EmailInput,ImageField

class Bookform(forms.ModelForm):
   date=forms.DateField()

   class Meta:
      model=Booking
      fields=['date']
    
class Chatform(forms.ModelForm):
    class Meta:
        model = Groupmessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add message...',
                'class': 'form-control form-control-lg',
                'id': 'textInput',
                'maxlength': '500',
                'autofocus': True,
                'style': 'border-radius: 20px; padding: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);'
            }),
        }

class NewGroupChatForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Group name',
                'class': 'form-control form-control-lg',
                'id': 'textInput',
                'autofocus': True,
                'max_length': '50',
                
            }),
        }

class ChatRoomEditForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name' : forms.TextInput(attrs={
                'class': 'form-control form-control-lg', 
                'maxlength' : '300', 
                }),
        }

class Userupdate(forms.ModelForm):
   email=forms.EmailField()

   class Meta:
      model =User
      fields=['username','email']
      widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Name'
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'placeholder': 'Email'
                })
        }
class Profileform(forms.ModelForm):
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': "form-control",
        'placeholder': 'Phone'
    }))
    review = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Review'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Address'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'State'
    }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': "form-control"
    }))

    class Meta:
        model = Profile  # Specify the model
        fields = ['image', 'phone', 'review', 'address', 'state']  # Specify the fields to include

class AvailabilityForm(forms.Form):
    Ammenity_CHOICES = (
        ("Buffet","Buffet"),
        ("Cafeteria-Style", "Cafeteria-Style"),
        ("Pre-Set Service", "Pre-Set Service"),
        ("Cocktail-Style", "Cocktail-Style"),
        ("Cabaret", "Cabaret"),
        ("Banquet-Style", "Banquet-Style"),
        ("Dinner-Dance", "Dinner-Dance"),
        ("Exhibition", "Exhibition"),
        ("Plated", "Plated"),
        ("Meeting-Style", "Meeting-Style"),
    )
    
    category_choices = (
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Grand", "Grand"),
        ("Deluxe", "Deluxe"), )
    SEAT_CHOICES = (
        ("2","2"),
        ("4", "4"),
        ("10", "10"),
        ("buffet", "buffet"),
    )
    category= forms.ChoiceField( choices=category_choices, widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    ammenity = forms.ChoiceField(
        choices=Ammenity_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    
    hallcapacity = forms.ChoiceField(
        choices=SEAT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    checkin = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        required=True
    )
    
    checkout = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        required=True
    )