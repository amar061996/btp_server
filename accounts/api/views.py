from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,

	)


from .serializers import (
	DriverListSerializer,
	DriverDetailSerializer,
	UserListSerializer,
	UserDetailSerializer
	)

from accounts.models import Drivers,UserProfile
from django.contrib.auth.models import User

################################################### DRIVERS VIEWS ###############################################################################
class DriverListView(ListAPIView):
	queryset=Drivers.objects.all()
	serializer_class=DriverListSerializer



class DriverDetailView(RetrieveAPIView):
	queryset=Drivers.objects.all()
	serializer_class=DriverDetailSerializer

################################################### USERS VIEWS ###############################################################################

class UserListView(ListAPIView):
	queryset=User.objects.all()
	serializer_class=UserListSerializer

class UserDetailSerializer(RetrieveAPIView):
	
	queryset=UserProfile.objects.all()
	serializer_class=UserDetailSerializer
	lookup_field='user__username'
	lookup_url_kwarg='username'
