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

from math import sin,cos,sqrt,atan2,radians

from datetime import datetime,timedelta

#calculate distance between coordinates

def calc_distance(lat1,lon1,lat2,lon2):

	rlat1 = radians(lat1)
 	rlon1 = radians(lon1)
 	rlat2 = radians(lat2)
 	rlon2 = radians(lon2)

 	dlat=(rlat2-rlat1)
 	dlon=(rlon2-rlon1)

 	a = sin(dlat / 2)**2 + cos(rlat1) * cos(rlat2) * sin(dlon / 2)**2
 	c = 2 * atan2(sqrt(a), sqrt(1 - a))

 	R=6373.0
 	distance=(R*c)*1000

 	return distance

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
		location=Location.objects.create(latitude=latitude,longitude=longitude,speed=speed,loc_type=loc_type,type_id=str(type_id))

		if loc_type=='user':
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
			'loc_type',
			'type_id',
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


class TransportNearbySerializer(ModelSerializer):
	location=SerializerMethodField()
	class Meta:
		model=User
		fields=[
			'username',
			'location',

		]

	def get_location(self,obj):

		user=obj
		
		
		user_all_location=Location.objects.filter(loc_type='user').filter(type_id=user.id).order_by('-timestamp')
		if len(user_all_location)==0:
			return LocationSerializer([],many=True).data
		ulatitude=user_all_location.first().latitude
		if ulatitude=='+1' or ulatitude=='-1':
			ulocation=user_all_location[1]
		else:
			ulocation=user_all_location.first()

		
		
		if ulocation:
			lat1=float(ulocation.latitude)
			lon1=float(ulocation.longitude)

			transports=Transport.objects.all()
			tlocations=list()

			for transport in transports:
				
				qs=Location.objects.filter(loc_type='transport').filter(type_id=transport.gps_id)
				

				if len(qs)==0:
					continue
				temp_loc=qs.last()

				lat2=float(temp_loc.latitude)
				lon2=float(temp_loc.longitude)

				distance=calc_distance(lat1,lon1,lat2,lon2)
				
				if distance<=2000.0:
					tlocations.append(temp_loc)
		else:
			tlocations=[]

		return LocationSerializer(tlocations,many=True).data









