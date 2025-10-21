from django.db import models
from django.contrib.auth.models import User



class Sitter(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    experience = models.IntegerField()
    specialty = models.CharField(max_length=500, blank=True)
    bio = models.CharField(max_length=1000, blank=True)
    rate = models.IntegerField(default=0)

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
    
class Owner_and_Sitter(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    experience = models.IntegerField()
    specialty = models.CharField(max_length=500, blank=True)
    bio = models.CharField(max_length=1000, blank=True)
    rate = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_and_sitter')
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} (Owner & Sitter)"

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
    species = models.CharField(max_length=50, choices=TYPE_CHOICES, default='dog')
    breed = models.CharField(max_length=100,)
    age = models.IntegerField()
    feed_schedule = models.CharField(max_length=100)
    medicine = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name='pets', default=2)
    owner_and_sitter = models.ForeignKey('Owner_and_Sitter', on_delete=models.CASCADE, null=True, blank=True, related_name='pets')

    def __str__(self):
        return f"{self.name} ({self.species})"

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
    sitter = models.ForeignKey(Sitter, on_delete=models.CASCADE, related_name='bookings_received', blank=True, null=True)
    owner_and_sitter = models.ForeignKey(Owner_and_Sitter, on_delete=models.CASCADE, related_name='bookings_received', null=True, blank=True)
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
    roles = models.CharField(max_length=10, choices=[('owner','Pet Owner'), ('sitter','Pet Sitter'), ('both','Owner & Sitter')])
    def __str__(self):
        return f"{self.user.username} ({self.role})"

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, roles='owner')