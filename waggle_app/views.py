from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import SignupForm, OwnerForm, SitterForm, BothForm
from django.http import HttpResponse

class Home(LoginView):
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