from __future__ import unicode_literals
from django.db import models

class User(models.Model):
	email = models.EmailField(max_length=30)
	username = models.CharField(max_length=30, default="username")
	password = models.CharField(max_length=30)

class Board(models.Model):
	tiles = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
		
