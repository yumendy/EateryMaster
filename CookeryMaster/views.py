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
	return render_to_response('index.html',{'username':username},context_instance = RequestContext(req))

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
		message.user = MyUser.objects.filter(user__username=username)[0]
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
	message = Message.objects.filter(pk = Id)[0]
	user = MyUser.objects.filter(user__username = username)[0]
	if user.permission < 2:
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
