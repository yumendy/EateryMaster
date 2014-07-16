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
class ImgForm(forms.Form):
	img = forms.ImageField()

def index(req):
	username = req.session.get('username','')
	school_list = School.objects.all()
	assessment_list = Assessment.objects.all()
	announcement_cat = Category.objects.get(id = 1)
	content = {'username':username,'school_list':school_list,'assessment_list':assessment_list,'announcement_cat':announcement_cat}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
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
		message.user = MyUser.objects.get(user__username = username)
		message.save()
	message_list = Message.objects.all()
	content = {'username':username, 'message_list':message_list}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	return render_to_response('guestbook.html',content,context_instance = RequestContext(req))

def about(req):
	username = req.session.get('username','')
	content = {'username':username,'noheader':False}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
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
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	return render_to_response('reply.html',content,context_instance = RequestContext(req))

def addrestaurant(req):
	status = ''
	can_add = True
	username = req.session.get('username','')
	user_list = MyUser.objects.filter(permission = 3)
	try:
		user = MyUser.objects.get(user__username = username)
		if user.permission < 4:
			status = 'no_permission'
			can_add = False
		schools = School.objects.filter(admin = user)
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
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
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
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
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
			window_list = Window.objects.filter(restaurant__school = user.school)
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
						desc = post['desc'], \
						isbreakfast = True if post.get('isbreakfast', '') == 'on' else False, \
						islunch = True if post.get('islunch', '') == 'on' else False, \
						issupper = True if post.get('issupper', '') == 'on' else False
						)
		if req.FILES:
			uf = ImgForm(post,req.FILES)
			if uf.is_valid():
				new_dish.img = uf.cleaned_data['img']
		new_dish.save()
		status = 'success'
	content = {'username':username,'noheader':True,'status':status,'can_add':can_add,'window_list':window_list}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	return render_to_response('adddish.html',content,context_instance = RequestContext(req))

def canteens(req):
	username = req.session.get('username','')
	Id = req.GET['id']
	restaurant = Restaurant.objects.get(pk = Id)
	window_list = Window.objects.filter(restaurant = restaurant)
	content = {'username':username,'window_list':window_list,'restaurant':restaurant}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	return render_to_response('canteens.html',content)

def windows(req):
	username = req.session.get('username','')
	Id = req.GET['id']
	window = Window.objects.get(pk = Id)
	dish_list = Dish.objects.filter(window = window)
	content = {'username':username,'dish_list':dish_list,'window':window}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	return render_to_response('windows.html',content)

def ave(lst, field, num):
	Sum = 0
	for item in lst:
		Sum += item.field
	return Sum * 1.0 / num

def dishes(req):
	username = req.session.get('username','')
	Id = req.GET['id']
	dish = Dish.objects.get(pk = Id)
	assessment_list = Assessment.objects.filter(dish = dish)
	num_of_ass = len(assessment_list)
	ave_taste = ave_service = ave_price = ave_level = 0
	if num_of_ass > 0:
		for item in assessment_list:
			ave_taste += item.taste
			ave_level += item.level
			ave_service += item.service
			ave_price += item.price
		ave_price /= num_of_ass
		ave_service /= num_of_ass
		ave_level /= num_of_ass
		ave_taste /= num_of_ass
	if req.POST:
		post = req.POST
		new_ass = Assessment( \
								taste = post['taste'], \
								service = post['service'], \
								price = post['price'], \
								level = post['level'], \
								dish = dish, \
								content = post['content'], \
								user = MyUser.objects.filter(user__username = username)[0], \
								)
		new_ass.save()
		return HttpResponseRedirect('/dishes/?id=' + str(Id))
	content = {'username':username,'dish':dish,'assessment_list':assessment_list,'num_of_ass':num_of_ass, \
				'ave_taste':ave_taste,'ave_service':ave_service,'ave_level':ave_level,'ave_price':ave_price}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	return render_to_response('dishes.html', content, context_instance = RequestContext(req))

def admin(request):
	'''
		1: ordinary user
		2: can add&delete&update&list dish
		3: can a&d&u&l window
		4: can adul restaurant
		5: can adul school
	'''
	username = request.session.get('username','')
	content = {'username':username}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
			content['permission'] = cur.permission
		return render_to_response('admin.html', content)
	return HttpResponseRedirect('/')

def userpanel(request):
	username = request.session.get('username','')
	content = {'username':username}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
		content['assessments'] = Assessment.objects.filter(user = cur)
		content['messages'] = Message.objects.filter(user = cur)
		return render_to_response('userpanel.html', content)
	return HttpResponseRedirect('/')

def recommend(request):
	username = request.session.get('username','')
	content = {'username':username}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	return render_to_response('recommend_choose.html', content)

def allassessments(request):
	username = request.session.get('username','')
	content = {'username':username, 'assessments': Assessment.objects.all()}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	return render_to_response('all_assessments.html', content)

def adminnews(request):
	username = request.session.get('username','')
	content = {'username':username}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
		if cur.permission < 3:
			return HttpResponseRedirect('/')
		if request.GET:
			if request.GET['act'] == 'show':
				if request.GET.has_key('category'):
					try:
						content['newslist'] = News.objects.filter(category = Category.objects.get(name = request.GET['category']))
						content['category'] = request.GET['category']
					except:
						return HttpResponse("No such category!")
				else:
					content['newslist'] = News.objects.all()
				return render_to_response('admin_news.html', content)
		else:
			content['newslist'] = News.objects.all()
			return render_to_response('admin_news.html', content)
	else:
		return HttpResponseRedirect('/')

def newsindex(request):
	#act = del, edit, add
	username = request.session.get('username','')
	content = {'username':username}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	content['catlist'] = Category.objects.all()
	return render_to_response('newsindex.html', content)

def shownews(request):
	username = request.session.get('username','')
	content = {'username':username}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
		content['news'] = News.objects.get(id = int(request.GET['id']))
		return render_to_response('shownews.html', content)
	return HttpResponseRedirect('/')

def delnews(request):
	pass

def editnews(request):
	pass

def addnews(request):
	pass

def addanno(request):
	pass