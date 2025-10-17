from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Pet Owner'),
        ('sitter', 'Pet Sitter'),
        ('both', 'Owner & Sitter'),
    ]
    user = models.OnetoOneField(User, on_delete=models.CASCADE)
    roles = models.CharField(max_length=10, choices=ROLE_CHOICES, default='owner')
    sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

class Sitter(models.Model):
    name = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=20)
    experience = models.IntegerField()
    specialty = models.CharField(max_length=500)
    bio = models.CharField(max_length=1000)

class Owner(models.Model):
    name = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=20)
    pets = models.ForeignKey(Pet, on_delete=models.CASCADE)