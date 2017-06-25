from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,

	)
from .serializers import LocationSerializer,UserLocationSerializer,UserLocationDetailSerializer
from location.models import Location,UserLocation,TransportLocation
from django.contrib.auth.models import User

from rest_framework import permissions

class LocationListView(ListAPIView):
	queryset=Location.objects.all()
	serializer_class=LocationSerializer
	permission_classes =(permissions.IsAuthenticatedOrReadOnly,)

class LocationCreateView(CreateAPIView):
	queryset=Location.objects.all()
	serializer_class=LocationSerializer


class UserLocationListView(ListAPIView):
	queryset=UserLocation.objects.all()
	serializer_class=UserLocationSerializer


class UserLocationDetailView(RetrieveAPIView):
	queryset=User.objects.all()
	serializer_class=UserLocationDetailSerializer
	lookup_field='username'
	lookup_url_kwarg='username'	