from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Location(models.Model):

	longitude=models.CharField(max_length=250)
	latitude=models.CharField(max_length=250)
	speed=models.CharField(max_length=250)
	timestamp=models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.longitude+","+self.latitude