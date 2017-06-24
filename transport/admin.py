from django.contrib import admin

# Register your models here.
from .models import Transport,TransportLocation

admin.site.register(Transport)
admin.site.register(TransportLocation)