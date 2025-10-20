from django.contrib import admin
from. models import Sitter, Owner, Pet, Booking, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Sitter)
admin.site.register(Owner)
admin.site.register(Pet)
admin.site.register(Booking)