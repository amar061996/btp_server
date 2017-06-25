from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
	SlugRelatedField,
	DateTimeField
	)

from location.models import Location,UserLocation,TransportLocation
from accounts.api.serializers import UserListSerializer
from django.contrib.auth.models import User

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
class UserLocationSerializer(ModelSerializer):

	user=UserListSerializer(read_only=True)
	location=LocationSerializer(read_only=True)

	class Meta:
		model=UserLocation
		fields=[
			'user',
			'location'

		]

class UserLocationDetailSerializer(ModelSerializer):
	
	location=SerializerMethodField()
	class Meta:
		model=User
		fields=[
			'username',
			'email',
			'location'

		]		

	def get_location(self,obj):

		user=obj
		location_id=UserLocation.objects.filter(user=user).values('location')
		location_qs=Location.objects.filter(id__in=location_id).order_by('-timestamp')
		location=LocationSerializer(location_qs,many=True).data
		return location