from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User

def getrecommend(idlist, dishlist, std):
	ret = [[0,0,0],[0,0,0],[0,0,0]]
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
					ret[0] = [b.id, l.id, s.id]
				elif i==1:
					offset[2] = offset[1]
					ret[2] = ret[1]
					offset[1] = s2
					ret[1] = [b.id, l.id, s.id]
				elif i==2:
					offset[2] = s2
					ret[2] = [b.id, l.id, s.id]
	return ret


def recommend(request):
	username = request.session.get('username','')
	content = {'username':username}
	if username:
		cur = MyUser.objects.get(user__username = username)
		content['userid'] = cur.id
		if cur.permission > 1:
			content['isadmin'] = True
	content["dishlist"] = Dish.objects.all()
	if request.POST:
		idlist = [int(x)-1 for x in request.POST['idlist'].strip().split(' ')]
		dishlist = Dish.objects.all()#[Dish.objects.filter(isbreakfast = True), Dish.objects.filter(islunch = True), Dish.objects.filter(issupper = True)]
		standard = [2700, 70, 360, 500, 100]
		result = getrecommend(idlist, dishlist, standard)
		content['result'] = result
		return render_to_response('recommend_result.html', content)
	
	return render_to_response('recommend_choose.html', content, context_instance = RequestContext(request))