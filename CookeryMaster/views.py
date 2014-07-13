from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.
def index(req):
	username = req.session.get('username','')
	school_list = School.objects.all()
	content = {'username':username,'school_list':school_list}
	return render_to_response('index.html',content,context_instance = RequestContext(req))

def signup(req):
	if req.session.get('username',''):
		return HttpResponseRedirect('/')
	status = ''
	if req.POST:
		post = req.POST
		passwd = post['passwd']
		repasswd = post['repasswd']
		if passwd != repasswd:
			status = 're_err'
		else:
			if User.objects.filter(username = post['username']):
				status = 'user_exist'
			else:
				newuser = User.objects.create_user( username = post['username'], \
													password = post['passwd'], \
													email = post['email'], \
													)
				newuser.save()
				new_myuser = MyUser(user = newuser, \
									permission = 1, \
									)
				new_myuser.save()
				status = 'success'
	content = {'noheader':True,'status':status}
	return render_to_response('signup.html',content,context_instance = RequestContext(req))

def login(req):
	if req.session.get('username',''):
		return HttpResponseRedirect('/')
	status = ''
	if req.POST:
		post = req.POST
		username = post['username']
		password = post['passwd']
		if User.objects.filter(username = username):
			user = auth.authenticate(username = username, password = password)
			if user is not None:
				if user.is_active:
					auth.login(req,user)
					req.session['username'] = username
					return HttpResponseRedirect('/')
				else:
					status = 'Not active'
			else:
				status = 'Password error'
		else:
			status = 'User do not exist'
	content = {'noheader':True,'status':status}
	return render_to_response('login.html',content,context_instance = RequestContext(req))

def logout(req):
    auth.logout(req)
    return HttpResponseRedirect("/")

def guestbook(req):
	username = req.session.get('username','')
	if req.POST:
		post = req.POST
		message = Message()
		message.title = post['title']
		message.content = post['content']
		message.user = MyUser.objects.get(user__username=username)
		message.save()
	message_list = Message.objects.all()
	content = {'username':username, 'message_list':message_list}
	return render_to_response('guestbook.html',content,context_instance = RequestContext(req))

def about(req):
	username = req.session.get('username','')
	content = {'username':username,'noheader':False}
	return render_to_response('about.html',content ,context_instance = RequestContext(req))

def reply(req):
	status = ''
	can_reply = True
	username = req.session.get('username','')
	Id = req.GET["id"]
	message = Message.objects.get(pk = Id)
	try:
		user = MyUser.objects.get(user__username = username)
		if user.permission < 2:
			status = 'no_permission'
			can_reply = False
	except:
		status = 'no_permission'
		can_reply = False
	if req.POST:
		post = req.POST
		re = Reply( content = post['reply_content'], \
					user = user, \
					message = message, \
			)
		re.save()
		status = 'success'
	content = {'username':username,'noheader':True,'message':message,'status':status,'can_reply':can_reply}
	return render_to_response('reply.html',content,context_instance = RequestContext(req))

def addrestaurant(req):
	status = ''
	can_add = True
	username = req.session.get('username','')
	schools = School.objects.all()
	user_list = MyUser.objects.filter(permission = 3)
	try:
		user = MyUser.objects.get(user__username = username)
		if user.permission < 4:
			status = 'no_permission'
			can_add = False
	except:
		status = 'no_permission'
		can_add = False
	if req.POST:
		post = req.POST
		new_restaurant = Restaurant(name = post['name'], \
									admin = MyUser.objects.get(pk = post['admin']), \
									school = School.objects.get(name = post['school']), \
			)
		new_restaurant.save()
		status = 'success'
	content = {'username':username,'noheader':True,'status':status,'can_add':can_add,'schools':schools,'user_list':user_list}
	return render_to_response('addrestaurant.html',content,context_instance = RequestContext(req))

def addwindow(req):
	status = ''
	can_add = True
	username = req.session.get('username','')
	user_list = []
	restaurant_list = []
	try:
		user = MyUser.objects.filter(user__username = username)[0]
	except:
		status = 'no_permission'
		can_add = False
	else:
		if user.permission < 3:
			status = 'no_permission'
			can_add = False
		else:
			user_list = MyUser.objects.filter(permission = 2)
			if user.permission == 3:
				restaurant_list = Restaurant.objects.filter(admin = user)
			elif user.permission == 4:
				print user.school
				restaurant_list = Restaurant.objects.filter(school = user.school)
			else:
				restaurant_list = Restaurant.objects.all()
	if req.POST:
		post = req.POST
		new_window = Window(name = post['name'], \
							floor = post['floor'], \
							restaurant = Restaurant.objects.get(pk = post['restaurant']), \
							admin = MyUser.objects.get(pk = post['admin']), \
							)
		new_window.save()
		status = 'success'
	content = {'username':username,'noheader':True,'status':status,'can_add':can_add,'user_list':user_list,'restaurant_list':restaurant_list}
	return render_to_response('addwindow.html',content,context_instance = RequestContext(req))


def adddish(req):
	status = ''
	can_add = True
	window_list = []
	username = req.session.get('username','')
	try:
		user = MyUser.objects.filter(user__username = username)[0]
	except:
		status = 'no_permission'
		can_add = False
	else:
		if user.permission == 5:
			window_list = Window.objects.all()
		elif user.permission == 4:
			window_list = Window.objects.filter(restaurent__school = user.school)
		elif user.permission == 3:
			window_list = Window.objects.filter(restaurant = user.restaurant)
		elif user.permission == 2:
			window_list = Window.objects.filter(admin = user)
		else:
			status = 'no_permission'
			can_add = False
	if req.POST:
		post = req.POST
		new_dish = Dish(name = post['name'], \
						window = Window.objects.get(pk = post['window']), \
						energy = post['energy'], \
						fat = post['fat'], \
						carbohydrate = post['carbohydrate'], \
						vb1 = post['vb1'], \
						vb2 = post['vb2'], \
						desc = post['desc'])
	c = {'username':username,'noheader':True,'status':status,'can_add':can_add,'window_list':window_list}
	return render_to_response('adddish.html',content,context_instance = RequestContext(req))