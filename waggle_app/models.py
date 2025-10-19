from django.db import models
from django.contrib.auth.models import User



class Sitter(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    experience = models.IntegerField()
    specialty = models.CharField(max_length=500, blank=True)
    bio = models.CharField(max_length=1000, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Sitter)"


class Owner(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Owner)"

class Pet(models.Model):
    TYPE_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'bird'),
        ('reptile', 'reptile'),
        ('fish', 'fish'),
        ('other', 'Other')
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, default='dog')
    breed = models.CharField(max_length=100,)
    age = models.IntegerField()
    feed_schedule = models.CharField(max_length=100)
    medicine = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name='pets')

    def __str__(self):
        return f"{self.name} ({self.type})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    booking_start = models.DateField('Start Date')
    booking_end = models.DateField('End Date')
    pets = models.ForeignKey(Pet, on_delete=models.CASCADE)
    message = models.CharField(max_length=2000, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='bookings_made')
    sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE, related_name='bookings_received')
    pets = models.ManyToManyField(Pet, related_name='bookings')

    def __str__(self):
        return f"Booking by {self.owner.name} with {self.sitter.name} ({self.status})"


class Profile(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Pet Owner'),
        ('sitter', 'Pet Sitter'),
        ('both', 'Owner & Sitter'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.CharField(max_length=10, choices=ROLE_CHOICES, default='owner')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='owner')

    def __str__(self):
        return f"{self.user.username} ({self.role})"