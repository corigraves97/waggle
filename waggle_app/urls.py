from django.urls import path
from .views import ProfileView, EditProfileView
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('setup_profile/', views.setup_profile, name='setup_profile'),
    path('', views.Home.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/edit_profile/', EditProfileView.as_view(), name='edit_profile'),
]