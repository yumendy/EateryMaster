from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MyUser(models.Model):
	user = models.OneToOneField(User)
	def __unicode__(self):
		return user.username

class School(models.Model):
	name = models.CharField(max_length = 128)
	admin = models.OneToOneField(MyUser)

	def __unicode__(self):
		return self.name

class Restaurant(models.Model):
	name = models.CharField(max_length = 128)
	School = models.ForeignKey(School)
	admin = models.OneToOneField(MyUser)

	def __unicode__(self):
		return self.name

class Window(models.Model):
	name = models.CharField(max_length = 64)
	floor = models.IntegerField()
	restaurant = models.ForeignKey(Restaurant)
	admin = models.OneToOneField(MyUser)

	def __unicode__(self):
		return self.name

class Dish(models.Model):
	name = models.CharField(max_length = 64)
	window = models.ForeignKey(Window)
	
	def __unicode__(self):
		return name