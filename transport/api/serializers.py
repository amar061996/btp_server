from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
	SlugRelatedField,
	HyperlinkedIdentityField,
	HyperlinkedRelatedField,
	)


from transport.models import Transport
from accounts.api.serializers import DriverDetailSerializer


transport_url=HyperlinkedIdentityField(view_name="transport-api:transport-detail")
class TransportListSerializer(ModelSerializer):
	url=transport_url
	class Meta:
		model=Transport
		fields=[
				'gps_id',
				'license_plate',
				'url',
				

		]


class TransportDetailSerializer(ModelSerializer):
	driver=DriverDetailSerializer(read_only=True)
	class Meta:
		model=Transport
		fields=[
				'gps_id',
				'license_plate',
				'driver'

		]		