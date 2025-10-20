from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .models import Sitter, Owner, Pet, Booking, Profile
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

class Home(LoginView):
    template_name = 'home.html'

def profile(request):
    return HttpResponse("Profile page works!")

def bookings(request):
    return HttpResponse("Bookings page works!")

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid sign-up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
