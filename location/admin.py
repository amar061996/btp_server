from django.contrib import admin

# Register your models here.
from .models import Location,TransportLocation,UserLocation

admin.site.register(Location)
admin.site.register(TransportLocation)
admin.site.register(UserLocation)