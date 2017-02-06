from __future__ import unicode_literals
from django.db import models

class User(models.Model):
	email = models.EmailField(max_length=30)
	username = models.CharField(max_length=30, default="username")
	password = models.CharField(max_length=30)
	board = models.CharField(max_length=70, default="RNBQKBNR.PPPPPPPP.eeeeeeee.eeeeeeee.eeeeeeee.eeeeeeee.pppppppp.rnbqkbnr")
	is_active = models.BooleanField(default=False)
	activation_code = models.CharField(max_length=100)

	def __str__(self):
		return self.username