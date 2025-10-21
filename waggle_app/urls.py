from django.urls import path
from .views import Home, ProfileView, EditProfileView, AddPetView, PetListView, EditPetView, PetDetailView, DeletePetView, UserDirectoryView, UserProfileView, BookingListView, BookingRequestView, IncomingBookingListView, LoginView
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('setup_profile/', views.setup_profile, name='setup_profile'),
    path('', views.Home.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/add_pet', AddPetView.as_view(), name='add_pet'),
    path('profile/pet_list', PetListView.as_view(), name='pet_list'),
    path('profile/pets/<int:pk>', PetDetailView.as_view(), name='pet_detail'),
    path('pets/<int:pk>/edit/', EditPetView.as_view(), name='edit_pet'),
    path('pets/<int:pk>/delete/', DeletePetView.as_view(), name='delete_pet'),
    path('directory/', UserDirectoryView.as_view(), name='user_directory'),
    path('directory/<int:pk>', UserProfileView.as_view(), name='user_profile'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/add_booking/<int:pk>', BookingRequestView.as_view(), name='add_booking'),
    path('bookings/incoming/', IncomingBookingListView.as_view(), name='incoming_bookings'),
]