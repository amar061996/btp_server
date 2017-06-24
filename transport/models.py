from __future__ import unicode_literals

from django.db import models

# Create your models here.
from accounts.models import Drivers
from location.models import Location
class Transport(models.Model):

	gps_id=models.IntegerField(primary_key=True)
	license_plate=models.CharField(max_length=250)
	driver=models.ForeignKey(Drivers,on_delete=models.CASCADE)


	def __str__(self):
		return self.driver.dname+" : "+str(self.gps_id)




class TransportLocation(models.Model):

	transport=models.ForeignKey(Transport,on_delete=models.CASCADE)
	location=models.ForeignKey(Location,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.transport.gps_id)+" : "+self.location.longitude+","+self.location.latitude 