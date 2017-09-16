
from rest_framework.serializers import (
	Serializer,
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

from transport.api.serializers import TransportListSerializer,TransportDetailSerializer

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


class JourneySerializer(Serializer):
	start=CharField(max_length=250)
	end=CharField(max_length=250)




class UserHistorySerializer(ModelSerializer):
	transport=SerializerMethodField()
	journey=SerializerMethodField()
	class Meta:
		model=User
		fields=[
			'username',
			'transport',
			'journey',

		]

	def get_transport(self,obj):

		user=obj
		user_locations=Location.objects.filter(loc_type='user',type_id=user.id)
		
		time_from=datetime.now()+timedelta(days=-1)
		time_to=datetime.now()

		user_locations_today=user_locations.filter(timestamp__gte=time_from,timestamp__lt=time_to)

		transport_locations=Location.objects.filter(loc_type='transport')
		transport_locations_today=transport_locations.filter(timestamp__gte=time_from,timestamp__lt=time_to)

		flag=0
		count=0
		transport_frequecy_dict=dict()
		transport_in_journeys=[]
		index=0
		journey_count=[0]
		for i in range(len(user_locations_today)):
			loc=user_locations_today[i]

			if(loc.latitude=='-1'):
				index+=1
				flag=1

				continue
			if(loc.latitude=='+1'):
				flag=0
				count=0
				new_loc=user_locations_today[i-1]
				min_t=new_loc.timestamp+timedelta(minutes=-1)
				max_t=new_loc.timestamp+timedelta(minutes=+1,seconds=+30)
				lat1=float(new_loc.latitude)
				lon1=float(new_loc.longitude)
				qs=transport_locations_today.filter(timestamp__gte=min_t,timestamp__lt=max_t)
				if len(qs)>0:
					temp=transport_frequecy_dict.keys()
					for obj in qs:
						if obj.type_id in temp:
							lat2=float(obj.latitude)
							lon2=float(obj.longitude)
							#print calc_distance(lat1,lon1,lat2,lon2)
							if calc_distance(lat1,lon1,lat2,lon2)<10:
								transport_in_journeys.append(Transport.objects.get(gps_id=int(obj.type_id)))
				
				if (len(transport_in_journeys)<1):
					if len(transport_frequecy_dict)>0:
						transport_frequecy_dict=sorted(transport_frequecy_dict.items(),key=lambda x:x[1])
						gps_id=int(transport_frequecy_dict[len(transport_frequecy_dict)-1])
						tobject=Transport.objects.filter(gps_id=gps_id)
						transport_in_journeys.append(tobject)


				journey_count.append(len(transport_in_journeys)-journey_count[index-1])

				transport_frequecy_dict=dict()

			if((flag==1)and(count<3)):
				min_t=loc.timestamp+timedelta(minutes=-1)
				max_t=loc.timestamp+timedelta(minutes=+1,seconds=+30)
				lat1=float(loc.latitude)
				lon1=float(loc.longitude)
				qs=transport_locations_today.filter(timestamp__gte=min_t,timestamp__lt=max_t)
				if len(qs)>0:
					for obj in qs:
						#print obj.type_id
						if obj.type_id in transport_frequecy_dict:
							lat2=float(obj.latitude)
							lon2=float(obj.longitude)
							#print calc_distance(lat1,lon1,lat2,lon2)
							if calc_distance(lat1,lon1,lat2,lon2)<10:
								transport_frequecy_dict[obj.type_id]+=1
						else:
							lat2=float(obj.latitude)
							lon2=float(obj.longitude)
							#print calc_distance(lat1,lon1,lat2,lon2)
							if calc_distance(lat1,lon1,lat2,lon2)<10:
								transport_frequecy_dict[obj.type_id]=1

				count+=1


		parsed_index=0        
		final_data=[]
		if len(transport_in_journeys)>0:
			id_qs=list()
			for obj in transport_in_journeys:
				id_qs.append(obj.gps_id)
			#print id_qs
			for j in range(1,len(journey_count)):
				current_journey_transport_count=journey_count[j]
				req=id_qs[parsed_index:parsed_index+current_journey_transport_count]
				parsed_index+=current_journey_transport_count
				qs=Transport.objects.filter(gps_id__in=req)
				final_data.append(TransportDetailSerializer(qs,many=True).data)
				
			return final_data

			
		else:
			
			return TransportDetailSerializer([],many=True).data



	def get_journey(self,obj):

		user=obj

		user_locations=Location.objects.filter(loc_type='user',type_id=user.id)
		
		time_from=datetime.now()+timedelta(days=-1)
		time_to=datetime.now()
		transport_journey_dict=dict()
		transport_journey_dict={'start':-1,'end':-1}
		transport_in_journeys=[]
		flag=0
		user_locations_today=user_locations.filter(timestamp__gte=time_from,timestamp__lt=time_to)
		
		for i in range(len(user_locations_today)):

			loc=user_locations_today[i]
			
			if(loc.latitude=='-1'):

				transport_journey_dict['start']=(
													user_locations_today[i+1].latitude+":"+user_locations_today[i+1].longitude+"-"+
													str(user_locations_today[i+1].timestamp.time().hour)+","+
													str(user_locations_today[i+1].timestamp.time().minute)+"-"+
													str(user_locations_today[i+1].timestamp.date().year)+","+
													str(user_locations_today[i+1].timestamp.date().month)+","+
													str(user_locations_today[i+1].timestamp.date().day)
												)

			if(loc.latitude=='+1'):
				
				transport_journey_dict['end']=(
													user_locations_today[i-1].latitude+":"+user_locations_today[i-1].longitude+"-"+
													str(user_locations_today[i-1].timestamp.time().hour)+","+
													str(user_locations_today[i-1].timestamp.time().minute)+"-"+
													str(user_locations_today[i-1].timestamp.date().year)+","+
													str(user_locations_today[i-1].timestamp.date().month)+","+
													str(user_locations_today[i-1].timestamp.date().day)
												)
				
				transport_in_journeys.append(transport_journey_dict)
				transport_journey_dict=dict()


		return JourneySerializer(transport_in_journeys,many=True).data









