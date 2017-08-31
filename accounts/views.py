from django.shortcuts import render

import json
from django.http import HttpResponse
from django.http import JsonResponse

#models
from django.contrib.auth.models import User
from .models import UserProfile
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
def home(request):

	return HttpResponse("Hii")

@csrf_exempt
def test(request):
	
	 
	# print request.method
	# print request.POST
	# print request.body
	if request.method=='POST':
		#POST DATA

		data=json.loads(request.body)
		username=data["username"]
		password=data["password"]
		first_name=data["first_name"]
		last_name=data["last_name"]
		email=data["email"]
		address=data["address"]
		contact=data["contact"]
		aadhar=data["aadhar"]
		photo=data["photo"]
		print(username,password,first_name,last_name,email,address,contact,aadhar,photo)
		#creating objects
		user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
		if user:
			user.set_password(password)
		else :
			return HttpResponse("Error Creating User")

		profile=UserProfile.objects.create(user=user,address=address,contact=contact,aadhar=aadhar,photo=photo)
		if profile:
			return JsonResponse(data)		

	print("This is GET")
	return HttpResponse("This is get bro")		