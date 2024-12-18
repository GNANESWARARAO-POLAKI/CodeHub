from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
# Create your views here.

def index(request):
    return render(request,'index.html')                                       

def register(request):   
    form = UserRegistrationForm()  # Create a blank form for GET requests
    return render(request, 'register.html', {'form': form})
