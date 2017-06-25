from django.shortcuts import render


from django.http import HttpResponse

#models
from django.contrib.auth.models import User
from .models import UserProfile
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
def home(request):

	return HttpResponse("Hii")

@csrf_exempt
def test(request):

	if request.method=='POST':
		#POST DATA
		username=request.POST["username"]
		password=request.POST["password"]
		first_name=request.POST["first_name"]
		last_name=request.POST["last_name"]
		email=request.POST["email"]
		address=request.POST["address"]
		contact=request.POST["contact"]
		aadhar=request.POST["aadhar"]
		photo=request.POST["photo"]

		#creating objects
		user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
		if user:
			user.set_password(password)
		else :
			return HttpResponse("Error Creating User")

		profile=UserProfile.objects.create(user=user,address=address,contact=contact,aadhar=aadhar,photo=photo)
		if profile:
			return HttpResponse("Created User")		

	print("This is GET")
	return HttpResponse("This is get")		