from __future__ import unicode_literals

from django.db import models

# Create your models here.
from accounts.models import Drivers

class Transport(models.Model):

	gps_id=models.IntegerField(primary_key=True)
	license_plate=models.CharField(max_length=250)
	driver=models.ForeignKey(Drivers,on_delete=models.CASCADE)


	def __str__(self):
		return self.driver.dname+" : "+str(self.gps_id)


