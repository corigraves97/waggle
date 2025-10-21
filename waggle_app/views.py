from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Pet, Owner, Owner_and_Sitter, Sitter, Booking
from .forms import SignupForm, OwnerForm, SitterForm, BothForm, PetForm, BookingForm
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class Home(TemplateView):
    template_name = 'home.html'

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('setup_profile')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def setup_profile(request):
    profile = request.user.profile
    owner_form = sitter_form = both_form = None

    if request.method == 'POST':
        if profile.roles == 'owner':
            owner_form = OwnerForm(request.POST, instance=getattr(request.user, 'owner', None))
        elif profile.roles == 'sitter':
            sitter_form = SitterForm(request.POST, instance=getattr(request.user, 'sitter', None))
        elif profile.roles == 'both':
            both_form = BothForm(request.POST, instance=getattr(request.user, 'owner_and_sitter', None))

        valid_owner = owner_form.is_valid() if owner_form else True
        valid_sitter = sitter_form.is_valid() if sitter_form else True
        valid_both = both_form.is_valid() if both_form else True

        if valid_owner and valid_sitter and valid_both:
            if owner_form:
                owner_instance = owner_form.save(commit=False)
                owner_instance.user = request.user
                owner_instance.save()
            if sitter_form:
                sitter_instance = sitter_form.save(commit=False)
                sitter_instance.user = request.user
                sitter_instance.save()
            if both_form:
                both_instance = both_form.save(commit=False)
                both_instance.user = request.user
                both_instance.save()
            return redirect('profile')
    else:
        if profile.roles == 'owner':
            owner_form = OwnerForm(instance=getattr(request.user, 'owner', None))
        elif profile.roles == 'sitter':
            sitter_form = SitterForm(instance=getattr(request.user, 'sitter', None))
        elif profile.roles == 'both':
            both_form = BothForm(instance=getattr(request.user, 'owner_and_sitter', None))

    return render(request, 'accounts/setup_profile.html', {
        'owner_form': owner_form,
        'sitter_form': sitter_form,
        'both_form': both_form,
        'role': profile.roles
    })

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('setup_profile')

class EditProfileView(UpdateView):
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        role = self.request.user.profile.roles
        if role == 'owner':
            return getattr(self.request.user, 'owner', None)
        elif role == 'sitter':
            return getattr(self.request.user, 'sitter', None)
        elif role == 'both':
            return getattr(self.request.user, 'owner_and_sitter', None)
        return None
    
    def get_form_class(self):
        role = self.request.user.profile.roles
        if role == 'owner':
            return OwnerForm
        elif role == 'sitter':
            return SitterForm
        elif role == 'both':
            return BothForm
        return None
    
    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return super().form_valid(form)
    
class AddPetView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/add_pet.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = self.request.user

        if hasattr(user, 'owner'):
            owner_instance = user.owner
            owner_and_sitter_instance = None

        elif hasattr(user, 'owner_and_sitter'):
            owner_and_sitter_instance = user.owner_and_sitter

            owner_instance, _ = Owner.objects.get_or_create(
                user=user,
                defaults={
                    "name": owner_and_sitter_instance.name,
                    "city": owner_and_sitter_instance.city,
                    "state": owner_and_sitter_instance.state,
                },
            )

        else:
            return reverse_lazy('profile')
        
        form.instance.owner = owner_instance
        if owner_and_sitter_instance:
            form.instance.owner_and_sitter = owner_and_sitter_instance

        return super().form_valid(form)
    
class PetListView(ListView):
    model = Pet
    template_name = 'pets/pet_list.html'
    context_object_name = 'pets'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "owner"):
            return Pet.objects.filter(owner=user.owner)
        if hasattr(user, "owner_and_sitter"):
            linked_owner = getattr(user.owner_and_sitter, "owner", None)
        if linked_owner:
            return Pet.objects.filter(owner=linked_owner)

        return Pet.objects.none()

class PetDetailView(DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html' 
    context_object_name = 'pet'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'owner'):
            return Pet.objects.filter(owner=user.owner)
        elif hasattr(user, 'owner_and_sitter'):
            return Pet.objects.filter(owner_and_sitter=user.owner_and_sitter)
        return Pet.objects.none()   


class EditPetView(UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/edit_pet.html'
    success_url = reverse_lazy('pet_list')

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'owner'):
            return Pet.objects.filter(owner=user.owner)
        elif hasattr(user, 'owner_and_sitter'):
            return Pet.objects.filter(owner_and_sitter = user.owner_and_sitter)
        return Pet.Objects.none()
    
class DeletePetView(DeleteView):
    model = Pet
    template_name = 'pets/delete_pet.html' 
    success_url = reverse_lazy('pet_list')

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'owner'):
            return Pet.objects.filter(owner=user.owner)
        elif hasattr(user, 'owner_and_sitter'):
            return Pet.objects.filter(owner_and_sitter=user.owner_and_sitter)
        return Pet.objects.none()
    
class UserDirectoryView(LoginRequiredMixin, ListView):
    template_name = 'users/user_directory.html'
    context_object_name = 'users'

    def get_queryset(self):
        owners_and_sitters = Owner_and_Sitter.objects.all()
        sitters = Sitter.objects.all()
        users = list(owners_and_sitters) + list(sitters)

        for user in users:
            if isinstance(user, Owner_and_Sitter):
                user.role = 'Owner & Sitter'
            elif isinstance(user, Sitter):
                user.role = 'Sitter'
            else:
                user.role = 'unknown'
        return users

    
class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'users/user_profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        user_id = self.kwargs.get('pk')
        print(user_id)
        try:
            return Owner_and_Sitter.objects.get(user__pk=user_id)
        except Owner_and_Sitter.DoesNotExist:
            pass
        try:
            return Sitter.objects.get(user__pk=user_id)
        except Sitter.DoesNotExist:
            pass
        try:
            return Owner.objects.get(user__pk=user_id)
        except Owner.DoesNotExist:
            raise

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object

        if isinstance(profile_user, Owner_and_Sitter):
            profile_user.role = "Owner & Sitter"
        elif isinstance(profile_user, Sitter):
            profile_user.role = "Sitter"
        else:
            profile_user.role = "Unknown"

        return context
    
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'owner'):
            return Booking.objects.filter(owner=user.owner).order_by('-booking_start')
        
        elif hasattr(user, 'owner_and_sitter'):
            owner_and_sitter = user.owner_and_sitter
            owner_instance, _ = Owner.objects.get_or_create(
                user=user,
                defaults={
                    'name': owner_and_sitter.name,
                    'city': owner_and_sitter.city,
                    'state': owner_and_sitter.state
                }
            )
            return Booking.objects.filter(
                owner=owner_instance
            ).union(
                Booking.objects.filter(sitter__user=user)
            ).order_by('-booking_start')

        elif hasattr(user, 'sitter'):
            return Booking.objects.filter(sitter=user.sitter).order_by('-booking_start')

        return Booking.objects.none()
    
class BookingRequestView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/add_booking.html'
    success_url = reverse_lazy('booking_list') 

    def form_valid(self, form):
        user = self.request.user

        if hasattr(user, 'owner'):
            owner_instance = user.owner
        elif hasattr(user, 'owner_and_sitter'):
            owner_and_sitter_instance = user.owner_and_sitter
            owner_instance, _ = Owner.objects.get_or_create(
                user=user,
                defaults={
                    "name": owner_and_sitter_instance.name,
                    "city": owner_and_sitter_instance.city,
                    "state": owner_and_sitter_instance.state,
                },
            )
        else:
            return redirect('profile') 

        form.instance.owner = owner_instance

        target_pk = self.kwargs.get('pk')
        sitter_instance = Sitter.objects.filter(pk=target_pk).first()
        if sitter_instance:
            form.instance.sitter = sitter_instance
        else:
            owner_and_sitter_instance = get_object_or_404(Owner_and_Sitter, pk=target_pk)
            form.instance.owner_and_sitter = owner_and_sitter_instance

        return super().form_valid(form)

class IncomingBookingListView(LoginRequiredMixin, ListView):
    template_name = 'bookings/incoming_bookings.html'
    context_object_name = 'incoming_bookings'

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'sitter'):
            return Booking.objects.filter(sitter=user.sitter).order_by('-booking_start')
        elif hasattr(user, 'owner_and_sitter'):
            return Booking.objects.filter(owner_and_sitter=user.owner_and_sitter).order_by('-booking_start')
        return Booking.objects.none()
    
