from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
	SlugRelatedField,
	HyperlinkedIdentityField,
	HyperlinkedRelatedField,
	
	)




from accounts.models import Drivers,UserProfile

from django.contrib.auth.models import User
################################################### DRIVERS SERIALIZERS ###############################################################################




driver_detail_url=HyperlinkedIdentityField(view_name='accounts-api:driver-detail')


class DriverListSerializer(ModelSerializer):
	url=driver_detail_url
	class Meta:
		model=Drivers
		fields=[

				'dname',
				'dlicense',
				'daadhar',
				'url',

		]

class DriverDetailSerializer(ModelSerializer):

 	dphoto=SerializerMethodField()
 	#dscan=SerializerMethodField()
 	class Meta:
 		model=Drivers
 		fields=[

				'dname',
				'dcontact',
				'daddress',
				'dlicense',
				'daadhar',
				'dphoto',
				#'dscan'


		]

	def get_dphoto(self,obj):
			try:

				dphoto=obj.dphoto

			except:

				dphoto=None

			return dphoto	

	#to get scan doc
	'''
	def get_dscan(self,obj):

		try:

			dscan=obj.dscan.name
		except:
			dscan=None

		return dscan				
	'''

############################################################### USERS SERIALIZERS #################################################################

user_detail_url=HyperlinkedIdentityField(view_name='accounts-api:user-detail',lookup_field='username')



class UserListSerializer(ModelSerializer):
	
	url=user_detail_url
	class Meta:
		model=User
		fields=[
				
				'username',
				'email',
				'first_name',
				'url',
				
				
		]

		



class UserDetailSerializer(ModelSerializer):
	username = serializers.CharField(source='user.username')
	email=serializers.EmailField(source='user.email')
	name=serializers.CharField(source='user.get_full_name')
	user_id=serializers.CharField(source='user.id')
	class Meta:
		model=UserProfile
		fields=[
				'user_id',
				'name',
				'username',
				'email',
				'contact',
				'address',
				'aadhar',
				'photo',

		]

		

				