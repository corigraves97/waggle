
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Owner, Sitter, Owner_and_Sitter, Pet, Booking, Message

class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('owner', 'Pet Owner'),
        ('sitter', 'Pet Sitter'),
        ('both', 'Owner & Sitter'),
    ]
    roles = forms.ChoiceField(choices=ROLE_CHOICES) 

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'roles')

    def save(self, commit=True):
        user = super().save(commit=commit)
        Profile.objects.create(user=user, roles=self.cleaned_data['roles'])
        return user

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'city', 'state']

class SitterForm(forms.ModelForm):
    class Meta:
        model = Sitter
        fields = ['name', 'city', 'state', 'experience', 'specialty', 'bio', 'rate']

class BothForm(forms.ModelForm):
    class Meta:
        model = Owner_and_Sitter
        fields = ['name', 'city', 'state', 'experience', 'specialty', 'bio', 'rate']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'feed_schedule', 'medicine', 'description']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pets', 'booking_start', 'booking_end', 'message']
        widgets = {
            'booking_start': forms.DateInput(attrs={'type': 'date'}),
            'booking_end': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows':3}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your message here'})
        }