from rest_framework.generics import CreateAPIView,ListAPIView
from .serializers import LocationSerializer
from location.models import Location

from rest_framework import permissions

class LocationListView(ListAPIView):
	queryset=Location.objects.all()
	serializer_class=LocationSerializer
	permission_classes =(permissions.IsAuthenticatedOrReadOnly,)

class LocationCreateView(CreateAPIView):
	queryset=Location.objects.all()
	serializer_class=LocationSerializer

	