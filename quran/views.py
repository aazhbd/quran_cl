
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

from django.template.context import RequestContext
from quran.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def viewHome(request):
	context = RequestContext(request)
	context.update({ 'msg_body' : "All Chapters", })
	chapters = Chapter.objects.all()
	context.update({ 'chapters' : chapters, })
	return render_to_response("home.html", context_instance=context)

def viewInfo(request):
	context = RequestContext(request)
	context.update({ 'msg_body' : "", })
	return render_to_response("info.html", context_instance=context)

def viewLogin(request):
	context = RequestContext(request)
	name = request.POST.get('name', None)
	email = request.POST.get('email', None)
	upass = request.POST.get('password', None)
	rpass = request.POST.get('rpass', None)
	captcha = request.POST.get('hiddenRecaptcha', None)

	if request.method == "POST":
		if email and upass:
			user = User.objects.create_user(email, email, upass)
			user.first_name = name
			user.save()
			context.update({ 'msg_body' : "The registration is successful, enter information to login", })
		else:
			context.update({ 'msg_body' : "The sign up information were invalid." + str(email) + str(upass), })
			return render_to_response("signup.html", context_instance=context)

	return render_to_response("login.html", context_instance=context)

def viewDiscuss(request):
	context = RequestContext(request)
	username = request.POST.get('email', None)
	password = request.POST.get('password', None)
	authenticated = False

	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			context.update({ 'msg_body' : "Login is successful, participate in discussions.", })
		else:
			context.update({ 'msg_body' : "The account is currently inactive, contact administrator.", })
	else:
		context.update({ 'msg_body' : "The username and password were incorrect.", })
		return render_to_response("login.html", context_instance=context)

	return render_to_response("discuss.html", context_instance=context)

def viewLogout(request):
	context = RequestContext(request)
	logout(request)
	context.update({ 'msg_body' : "You have been logged out.", })
	return render_to_response("login.html", context_instance=context)

def viewSignup(request):
	context = RequestContext(request)
	return render_to_response("signup.html", context_instance=context)