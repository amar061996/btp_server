from django.contrib import admin

# Register your models here.
from .models import Drivers,UserProfile,UserContact

admin.site.register(Drivers)
admin.site.register(UserProfile)
admin.site.register(UserContact)