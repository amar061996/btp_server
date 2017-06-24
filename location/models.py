from __future__ import unicode_literals

from django.db import models

from transport.models import Transport
from django.contrib.auth.models import User
# Create your models here.
class Location(models.Model):

	longitude=models.CharField(max_length=250)
	latitude=models.CharField(max_length=250)
	speed=models.CharField(max_length=250)
	timestamp=models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.longitude+","+self.latitude




class TransportLocation(models.Model):

	transport=models.ForeignKey(Transport,on_delete=models.CASCADE)
	location=models.ForeignKey(Location,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.transport.gps_id)+" : "+self.location.longitude+","+self.location.latitude 		


class UserLocation(models.Model):
	
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	location=models.ForeignKey(Location,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username+" : "+self.location.longitude+","+self.location.latitude