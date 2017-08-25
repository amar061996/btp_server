from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
	SlugRelatedField,
	DateTimeField,
	CharField,
	IntegerField,
	)

from location.models import Location,UserLocation,TransportLocation
from accounts.api.serializers import UserListSerializer
from django.contrib.auth.models import User
from transport.models import Transport

from transport.api.serializers import TransportListSerializer

class LocationCreateSerializer(ModelSerializer):
	
	loc_type=CharField(max_length=250)
	type_id=IntegerField(min_value=0)
	class Meta:
		model=Location
		fields=[
			'id',
			'latitude',
			'longitude',
			'speed',
			'loc_type',
			'type_id'
			


		]

	def create(self,validated_data):
		
		type_id=validated_data.get('type_id')
		longitude=validated_data.get("longitude")
		latitude=validated_data.get("latitude")
		speed=validated_data.get("speed")
		loc_type=validated_data.get('loc_type')
		print(longitude)
		location=Location.objects.create(latitude=latitude,longitude=longitude,speed=speed)

		if loc_type=='user':
			print("hello")
			user=User.objects.filter(id=type_id).first()
			created_user=UserLocation.objects.create(user=user,location=location)
		else:
			transport=Transport.objects.filter(gps_id=type_id).first()
			TransportLocation.objects.create(transport=transport,location=location)
		return {"id":location.id,"latitude":location.latitude,"longitude":location.longitude,"speed":location.speed,"loc_type":loc_type,'type_id':type_id}


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

	# def create(self,validated_data):
	# 	longitude=validated_data.get("longitude")
	# 	latitude=validated_data.get("latitude")
	# 	speed=validated_data.get("speed")
	# 	location=Location.objects.create(latitude=latitude,longitude=longitude,speed=speed)
	# 	return location




class UserLocationSerializer(ModelSerializer):

	user=UserListSerializer()
	location=LocationSerializer()

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


class TransportLocationSerializer(ModelSerializer):
	transport=TransportListSerializer()
	location=LocationSerializer()
	class Meta:
		model=TransportLocation
		fields=[

			'transport',
			'location'
		]		



class TransportLocationDetailSerializer(ModelSerializer):
	
	location=SerializerMethodField()
	class Meta:
		model=Transport	
		fields=[
			'gps_id',
			'license_plate',
			'location'

		]	

	def get_location(self,obj):

		transport=obj
		location_id=TransportLocation.objects.filter(transport=transport).values('location')
		location_qs=Location.objects.filter(id__in=location_id).order_by('-timestamp')
		location=LocationSerializer(location_qs,many=True).data
		return location