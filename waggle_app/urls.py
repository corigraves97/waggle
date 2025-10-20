from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('profile/', views.profile, name='profile'),
    path('bookings/', views.bookings, name='bookings'),
]