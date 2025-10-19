from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .models import Sitter, Owner, Pet, Booking, Profile
from django.urls import reverse
from django.http import HttpResponse

def home(request):
    return render(request, 'waggle_app/home.html')

def profile(request):
    return HttpResponse("Profile page works!")

def bookings(request):
    return HttpResponse("Bookings page works!")