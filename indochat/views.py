from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import HttpResponseBadRequest,Http404
from datetime import datetime,timedelta
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login 
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views import View
from bongapp.models import *
# Create your views here.
def chat_view(request):
    return render(request,'chat.html')