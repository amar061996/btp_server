from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
	SlugRelatedField,
	DateTimeField
	)

from location.models import Location


class LocationSerializer(ModelSerializer):
	
	timestamp=DateTimeField(format="%d-%m-%Y %H:%M:%S")
	class Meta:
		model=Location
		fields=[
			'id',
			'latitude',
			'longitude',
			'speed',
			'timestamp',


		]
