from django.shortcuts import *
from django.http import *
from .models import User


def home(request):
	#if(request.session.get('username', 0) == 0):
	return render(request, "chess/home.html", {'login_error': "", 'register_error': ""})
	#else:
	#return HttpResponseRedirect("/chess/game")

def login(request):
	try:
		user = User.objects.get(email=request.POST['email'].lower(), password=request.POST['password'])
		#request.session['username'] = user.username
		return HttpResponseRedirect("/chess/game")
	except:
		return render(request, "chess/home.html", {'login_error': "No user found!", 'register_error': ""})

def register(request):
	if(not User.objects.filter(username=request.POST['username']) and not User.objects.filter(email=request.POST['email'])):
		user = User(username=request.POST['username'].lower(), password=request.POST['password'], email=request.POST['email'].lower())
		user.save()
		return HttpResponse("<h1>User Added !</h1>")
	else:
		return render(request, 'chess/home.html', {'register_error': "username or email already Exists !", 'login_error': ""})

def game(request):
	user = User.objects.get(username='mamzi')
	return render(request, 'chess/game.html')