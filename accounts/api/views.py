from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,

	)


from .serializers import DriverListSerializer,DriverDetailSerializer
from accounts.models import Drivers

class DriverListView(ListAPIView):
	queryset=Drivers.objects.all()
	serializer_class=DriverListSerializer



class DriverDetailView(RetrieveAPIView):
	queryset=Drivers.objects.all()
	serializer_class=DriverDetailSerializer
	
