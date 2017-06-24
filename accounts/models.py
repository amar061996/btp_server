from __future__ import unicode_literals

from django.db import models


from django.contrib.auth.models import User
# Create your models here.

def upload_photo(instance,filename):

	return "%s/%s"%("drivers_photo",filename)

def upload_file(instance,filename):

	return "%s/%s"%("drivers_file",filename)	

def upload_user(instance,filename):

	return "%s/%s"%("user_photo",filename)	

class Drivers(models.Model):

	dname=models.CharField(max_length=250)
	dcontact=models.CharField(max_length=250)
	daddress=models.TextField()
	dlicense=models.CharField(max_length=250)
	daadhar=models.DecimalField(max_digits=12,decimal_places=0)
	dphoto=models.ImageField(upload_to=upload_photo)
	dscan=models.FileField(upload_to=upload_file)


	def __str__(self):

		return self.dname+" : "+str(self.daadhar)





class UserProfile(models.Model):

	user=models.OneToOneField(User,on_delete=models.CASCADE)
	photo=models.ImageField(upload_to=upload_user)
	address=models.TextField()
	contact=models.CharField(max_length=250)
	aadhar=models.DecimalField(max_digits=12,decimal_places=0)

	def __str__(self):
		return self.user.username