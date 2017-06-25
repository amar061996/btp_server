from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
	SlugRelatedField,
	HyperlinkedIdentityField
	
	)




from accounts.models import Drivers



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
 	dscan=SerializerMethodField()
 	class Meta:
 		model=Drivers
 		fields=[

				'dname',
				'dcontact',
				'daddress',
				'dlicense',
				'daadhar',
				'dphoto',
				'dscan'


		]

	def get_dphoto(self,obj):
			try:

				dphoto=obj.dphoto.url

			except:

				dphoto=None

			return dphoto	

	def get_dscan(self,obj):

		try:
			dscan=obj.dscan.url
		except:
			dscan=None

		return dscan				