from django.shortcuts import *
from django.http import *
from .models import User


def home(request):
	return render(request, "chess/home.html", {'login_error': "", 'register_error': ""})

def login(request):
	try:
		user = User.objects.get(email=request.POST['email'].lower(), password=request.POST['password'])
	except:
		return render(request, "chess/home.html", {'login_error': "No user found!", 'register_error': ""})
	else:
		return HttpResponse("GAME")

def register(request):
	return render(request, "chess/home.html")

#def register(request):	


