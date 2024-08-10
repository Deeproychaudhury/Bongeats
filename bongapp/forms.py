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
   phone=forms.IntegerField()
   review=forms.CharField()
   address = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Address'
    }))    
   state = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'State'
    }))

   class Meta:
      model=Profile
      fields= ['image','phone','review','address','state']
      widgets = {
            'review': TextInput(attrs={
                'class': "form-control",
                'style': 'style="color :#A82C48"',
                'placeholder': 'Name'
                }),
            'phone': EmailInput(attrs={
                'class': "form-control", 
                'placeholder': 'Email'
                })
        }