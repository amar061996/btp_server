from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,

	)


from .serializers import TransportListSerializer,TransportDetailSerializer

from transport.models import Transport


class TransportListView(ListAPIView):

	queryset=Transport.objects.all()
	serializer_class=TransportListSerializer



class TransportDetailView(RetrieveAPIView):
	
	queryset=Transport.objects.all()
	serializer_class=TransportDetailSerializer	

