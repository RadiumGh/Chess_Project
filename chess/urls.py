from django.conf.urls import *
from .views import *

urlpatterns = [
	url(r'^login/$', login, name='login'),
	url(r'^register/$', register, name='register'),
	url(r'^$', home, name='home'),
	url(r'^game/$', game, name='game'),
	url(r'^game/move/$', move, name='move'),
	url(r'^active/$', active, name='active'), 
	url(r'^signout/$', sign_out, name='signout')
]