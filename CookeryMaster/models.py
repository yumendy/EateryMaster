from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MyUser(models.Model):
	user = models.OneToOneField(User)
	def __unicode__(self):
		return user.username

class Restaurant(models.Model):
	name = models.CharField(max_length = 128)
	location = models.CharField(max_length = 512)
	admin = models.OneToOneField(MyUser)

	def __unicode__(self):
		return self.name

class Floor(models.Model):
	name = models.CharField(max_length = 16)
	restaurant = models.ForeignKey(Restaurant)

	def __unicode__(self):
		return restaurant.name + '-' + name

class Window(models.Model):
	name = models.CharField(max_length = 64)
	Floor = models.ForeignKey(Floor)
	admin = models.OneToOneField(MyUser)

	def __unicode__(self):
		return Floor.restaurant.name + '-' + Floor.name + '-' + name

class Dish(models.Model):
	name = models.CharField(max_length = 64)
	window = models.ForeignKey(Window)

	def __unicode__(self):
		return name

