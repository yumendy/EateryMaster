from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MyUser(models.Model):
	user = models.OneToOneField(User)
	permission = models.IntegerField()
	def __unicode__(self):
		return self.user.username

class School(models.Model):
	name = models.CharField(max_length = 128)
	admin = models.OneToOneField(MyUser)

	def __unicode__(self):
		return self.name

class Restaurant(models.Model):
	name = models.CharField(max_length = 128)
	school = models.ForeignKey(School)
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
	energy = models.FloatField() #kcal
	fat = models.FloatField() #gram
	carbohydrate = models.FloatField() #gram
	vb1 = models.FloatField() #mg
	vb2 = models.FloatField() #ug
	desc = models.CharField(max_length = 500)
	img = models.ImageField(upload_to= './image/')

	def __unicode__(self):
		return self.name

class Message(models.Model):
	title = models.CharField(max_length = 50)
	content = models.CharField(max_length = 512)
	user = models.ForeignKey(MyUser)
	create_datetime = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.title

class Reply(models.Model):
	content = models.CharField(max_length = 200)
	user = models.ForeignKey(MyUser)
	message = models.ForeignKey(Message)
	create_datetime = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.content

class Assessment(models.Model):
	content = models.CharField(max_length = 500)
	taste = models.IntegerField()
	service = models.IntegerField()
	price = models.IntegerField()
	level = models.IntegerField()
	dish = models.ForeignKey(Dish)
	user = models.ForeignKey(MyUser)
	create_datetime = models.DateTimeField()

	def __unicode__(self):
		return self.content

class News(models.Model):
	user = models.ForeignKey(MyUser)
	title = models.CharField(max_length = 64)
	content = models.CharField(max_length = 512)
	category = models.ForeignKey(Category)
	time = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.title

class Category(models.Model):
	name = models.CharField(max_length = 32)

	def __unicode__(self):
		return self.name
