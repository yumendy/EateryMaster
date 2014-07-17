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
	announcement_cat = Category.objects.get(id = 2)
	content = {'username':username,'school_list':school_list,'assessment_list':assessment_list,'active_item':'homepage','announcement_cat':announcement_cat}
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
	content = {'username':username, 'message_list':message_list,'active_item':'gust'}
	return render_to_response('guestbook.html',content,context_instance = RequestContext(req))

def about(req):
	username = req.session.get('username','')
	content = {'username':username,'noheader':False,'active_item':'about'}
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
	user_list = MyUser.objects.filter(permission = 3)
	try:
		user = MyUser.objects.get(user__username = username)
		permission = user.permission
		if user.permission < 4:
			status = 'no_permission'
			can_add = False
	except:
		status = 'no_permission'
		can_add = False
	if permission == 4:
		schools = School.objects.filter(admin = user)
	elif permission == 5:
		schools = School.objects.all()
	if req.POST:
		post = req.POST
		new_restaurant = Restaurant(name = post['name'], \
									admin = MyUser.objects.get(pk = post['admin']), \
									school = School.objects.get(name = post['school']), \
			)
		new_restaurant.save()
		status = 'success'
	category_list = Category.objects.all()
	content = {'username':username,'status':status,'can_add':can_add,'schools':schools,'user_list':user_list, \
	'category_list':category_list,'permission':permission,'active_item':"addrest"}
	return render_to_response('addrestaurant2.html',content,context_instance = RequestContext(req))

def addwindow(req):
	status = ''
	can_add = True
	username = req.session.get('username','')
	user_list = []
	restaurant_list = []
	try:
		user = MyUser.objects.filter(user__username = username)[0]
		permission = user.permission
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
	category_list = Category.objects.all()
	content = {'username':username,'status':status,'can_add':can_add,'user_list':user_list, \
				'restaurant_list':restaurant_list,'permission':permission,'category_list':category_list,'active_item':"addwin"}
	return render_to_response('addwindow2.html',content,context_instance = RequestContext(req))


def adddish(req):
	status = ''
	can_add = True
	window_list = []
	username = req.session.get('username','')
	try:
		user = MyUser.objects.filter(user__username = username)[0]
		permission = user.permission
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
						desc = post['desc'],\
						isbreakfast = post.get('isbreakfast',False), \
						islunch = post.get('islunch',False), \
						issupper = post.get('issupper',False), \
						)
		if req.FILES:
			uf = ImgForm(post,req.FILES)
			if uf.is_valid():
				new_dish.img = uf.cleaned_data['img']
		new_dish.save()
		status = 'success'
	category_list = Category.objects.all()
	content = {'username':username,'status':status,'can_add':can_add,'window_list':window_list, \
	'permission':permission,'category_list':category_list,'active_item':"adddish"}
	return render_to_response('adddish2.html',content,context_instance = RequestContext(req))

def canteens(req):
	username = req.session.get('username','')
	Id = req.GET['id']
	restaurant = Restaurant.objects.get(pk = Id)
	window_list = Window.objects.filter(restaurant = restaurant)
	content = {'username':username,'window_list':window_list,'restaurant':restaurant}
	return render_to_response('canteens.html',content)

def windows(req):
	username = req.session.get('username','')
	Id = req.GET['id']
	window = Window.objects.get(pk = Id)
	dish_list = Dish.objects.filter(window = window)
	content = {'username':username,'dish_list':dish_list,'window':window}
	return render_to_response('windows.html',content)

def dishes(req):
	username = req.session.get('username','')
	Id = req.GET.get('id','')
	if Id == '':
		dish_list = Dish.objects.all()
		return render_to_response('alldishes.html',{'username':username,'dish_list':dish_list})
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
	return render_to_response('dishes.html', content, context_instance = RequestContext(req))

def allassessment(req):
	username = req.session.get('username','')
	assessment_list = Assessment.objects.all()
	dish_list = Dish.objects.all()
	content = {'username':username,'assessment_list':assessment_list,'dish_list':dish_list,'active_item':"ass"}
	return render_to_response('allass.html',content)

def overview(req):
	username = req.session.get('username','')
	if username == '':
		return HttpResponseRedirect('/')
	user = MyUser.objects.get(user__username = username)
	category_list = Category.objects.all()
	assessment_list = Assessment.objects.filter(user = user)
	message_list = Message.objects.filter(user = user)
	permission = user.permission
	content = {'username':username,'category_list':category_list,'permission':permission,'assessment_list':assessment_list, \
	'message_list':message_list,'active_item':"overview"}
	return render_to_response('overview.html',content)

def addanno(req):
	username = req.session.get('username','')
	try:
		user = MyUser.objects.filter(user__username = username)[0]
		permission = user.permission
	except:
		return HttpResponseRedirect('/')
	if user.permission < 3:
		return HttpResponseRedirect('/')
	if req.POST:
		post = req.POST
		new_anno = News( \
						user = user, \
						title = post['title'], \
						content = post['content'], \
						category = Category.objects.get(pk = 2))
		new_anno.save()
	category_list = Category.objects.all()
	content = {'username':username,'permission':permission,'category_list':category_list,'active_item':"addanno"}
	return render_to_response('addanno.html',content,context_instance = RequestContext(req))

def disheslist(req):
	username = req.session.get('username','')
	try:
		user = MyUser.objects.filter(user__username = username)[0]
		permission = user.permission
	except:
		return HttpResponseRedirect('/')
	if user.permission < 2:
		return HttpResponseRedirect('/')
	if permission == 2:
		window_list = Window.objects.filter(admin = user)
	elif permission == 3:
		window_list = Window.objects.filter(restaurant = user.restaurant)
	elif permission == 4:
		window_list = Window.objects.filter(restaurant__school = user.school)
	elif permission == 5:
		window_list = Window.objects.all()
	category_list = Category.objects.all()
	content = {'username':username,'window_list':window_list,'category_list':category_list,'permission':permission, \
	'active_item':"dishlist"}
	return render_to_response('disheslist.html',content)

def windowlist(req):
	username = req.session.get('username','')
	try:
		user = MyUser.objects.filter(user__username = username)[0]
		permission = user.permission
	except:
		return HttpResponseRedirect('/')
	if user.permission < 3:
		return HttpResponseRedirect('/')
	if permission == 3:
		restaurant_list = Restaurant.objects.filter(admin = user)
	elif permission == 4:
		restaurant_list = Restaurant.objects.filter(school = user.school)
	elif permission == 5:
		restaurant_list = Restaurant.objects.all()
	category_list = Category.objects.all()
	content = {'username':username,'restaurant_list':restaurant_list,'category_list':category_list,'permission':permission,'active_item':"winlist"}
	return render_to_response('windowlist.html',content)

def restaurantlist(req):
	username = req.session.get('username','')
	try:
		user = MyUser.objects.filter(user__username = username)[0]
		permission = user.permission
	except:
		return HttpResponseRedirect('/')
	if user.permission < 4:
		return HttpResponseRedirect('/')
	if permission == 4:
		school_list = School.objects.filter(admin = user)
	elif permission == 5:
		school_list = School.objects.all()
	category_list = Category.objects.all()
	content = {'username':username,'school_list':school_list,'category_list':category_list,'permission':permission,\
	'active_item':"restlist"}
	return render_to_response('restaurantlist.html',content)

def newsindex(req):
	username = req.session.get('username','')
	category_list = Category.objects.all()
	content = {'username':username,'category_list':category_list,'active_item':'zixun'}
	return render_to_response('shownews.html',content)

def addnews(req):
	username = req.session.get('username','')
	try:
		user = MyUser.objects.filter(user__username = username)[0]
	except:
		return HttpResponseRedirect('/')
	if req.POST:
		post = req.POST
		new_anno = News( \
						user = user, \
						title = post['title'], \
						content = post['content'], \
						category = Category.objects.get(pk = 1))
		new_anno.save()
	category_list = Category.objects.all()
	content = {'username':username,'active_item':"zixun"}
	return render_to_response('addnews.html',content,context_instance = RequestContext(req))

def newsdetail(req):
	username = req.session.get('username','')
	Id = req.GET['id']
	try:
		news = News.objects.get(pk = Id)
	except:
		return HttpResponseRedirect('/news/index/')
	content = {'username':username,'news':news,'active_item':'zixun'}
	return render_to_response('newsdetail.html',content)

"""
the core code of dishes recommend written by xivid
"""

def getrecommend(idlist, dishlist, std):
	ret = [[1,1,1],[1,1,1],[1,1,1]]
	day3 = [sum([dishlist[id].energy for id in idlist]), \
		  sum([dishlist[id].fat for id in idlist]), \
		  sum([dishlist[id].carbohydrate for id in idlist]), \
		  sum([dishlist[id].vb1]), \
		  sum([dishlist[id].vb2])]
	b_list = [dish for dish in dishlist if dish.isbreakfast == True] #breakfast
	l_list = [dish for dish in dishlist if dish.islunch == True] #lunch
	s_list = [dish for dish in dishlist if dish.issupper == True] #supper
	offset = [10,10,10]
	for b in b_list:
		for l in l_list:
			for s in s_list:
				n1 = (day3[0]+b.energy+l.energy+s.energy)/4.0/std[0]
				n2 = (day3[1]+b.fat+l.fat+s.fat)/4.0/std[1]
				n3 = (day3[2]+b.carbohydrate+l.carbohydrate+s.carbohydrate)/4.0/std[2]
				n4 = (day3[3]+b.vb1+l.vb1+s.vb1)/4.0/std[3]
				n5 = (day3[4]+b.vb2+l.vb2+s.vb2)/4.0/std[4]
				s2 = ((n1-1.0)**2 + (n2-1.0)**2 + (n3-1.0)**2 + (n4-1.0)**2 + (n5-1.0)**2)
				i = 3
				while i > 0 and s2 < offset[i-1]:
					i -= 1
				if i==0:
					offset[2] = offset[1]
					ret[2] = ret[1]
					offset[1] = offset[0]
					ret[1] = ret[0]
					offset[0] = s2
					ret[0] = [b.id+1, l.id+1, s.id+1]
				elif i==1:
					offset[2] = offset[1]
					ret[2] = ret[1]
					offset[1] = s2
					ret[1] = [b.id+1, l.id+1, s.id+1]
				elif i==2:
					offset[2] = s2
					ret[2] = [b.id+1, l.id+1, s.id+1]
	return ret

def recommend(request):
	username = request.session.get('username','')
	content = {'username':username,'active_item':'recom'}
	content["dishlist"] = Dish.objects.all()
	if request.POST:
		idlist = [int(x)-1 for x in request.POST['idlist'].strip().split(' ')]
		dishlist = Dish.objects.all()#[Dish.objects.filter(isbreakfast = True), Dish.objects.filter(islunch = True), Dish.objects.filter(issupper = True)]
		standard = [2700, 70, 360, 500, 100]
		result = getrecommend(idlist, dishlist, standard)
		for x in xrange(0, 3):
			for y in xrange(0,3):
				result[x][y] = Dish.objects.get(pk = result[x][y])
		content['result'] = result
		return render_to_response('recommend_result2.html', content)

	return render_to_response('recommend_choose.html', content, context_instance = RequestContext(request))