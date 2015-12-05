
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

from django.template.context import RequestContext
from django.db.models import Q,Count, Min, Max, Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from quran.models import *
import json


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

	if request.method == "POST":
		name = request.POST.get('name', None)
		email = request.POST.get('email', None)
		upass = request.POST.get('password', None)
		rpass = request.POST.get('rpass', None)
		captcha = request.POST.get('hiddenRecaptcha', None)

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

	if request.method == "POST":
		username = request.POST.get('email', None)
		password = request.POST.get('password', None)

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				context.update({ 'msg_body' : "Login is successful.", })
			else:
				context.update({ 'msg_body' : "The account is currently inactive, contact administrator.", })
		else:
			context.update({ 'msg_body' : "The username and password were incorrect.", })
			return render_to_response("login.html", context_instance=context)

	context.update({ 'msg_body' : "Participate in discussions.", })
	return render_to_response("discuss.html", context_instance=context)

def viewLogout(request):
	context = RequestContext(request)
	logout(request)
	context.update({ 'msg_body' : "You have been logged out.", })
	return render_to_response("login.html", context_instance=context)

def viewSignup(request):
	context = RequestContext(request)
	return render_to_response("signup.html", context_instance=context)

def viewChapter(request, **Args):
	context = RequestContext(request)

	chapterNum = str(Args.get('chap')).strip('/')
	cNum = str(chapterNum)
	context.update({ 'cnum' : cNum, })

	try:
		chName = Chapter.objects.get(pk=cNum)
		context.update({ 'msg_body' : "All verses of the chapter " + cNum + ": " + chName.transliteration + " " + chName.arabic_name + " (" + chName.english_name + ")", })
	except:
		context.update({ 'msg_body' : "Invalid chapter number", })

	v = Q(chapter=cNum) & Q(author__name='Original Text')
	full_chap = Verse.objects.filter(v).order_by('number')
	context.update({ 'full_chap' : full_chap, })

	auths = Verse.objects.filter(chapter=cNum).values('author').distinct()
	authors = []
	for a in auths:
		authors.append(Author.objects.get(pk=a['author']))

	context.update({ 'authors' : authors, })

	return render_to_response("chapter.html", context_instance=context)

def viewVerse(request, **Args):
	context = RequestContext(request)

	cSuccess = False

	chapterNum = str(Args.get('chap')).strip('/')
	verseNum = str(Args.get('verse')).strip('/')

	cNum = str(chapterNum)
	vNum = str(verseNum)

	cf_init = dict(user=request.user.pk, vnum=vNum, cnum=cNum)

	if(request.method=="POST"):
		post = request.POST.copy()

		# comment_form = VerseCommentForm(request.POST, initial=cf_init)

		if(comment_form.is_valid()):
			try:
				newComment = comment_form.save()
				cSuccess = True
			except:
				context.update({ 'messages' : "comment save failed.", })
				raise
		else:
			context.update({ 'messages' : "comment save failed.", })
	else:
		pass
		# comment_form = VerseCommentForm(initial=cf_init)


	context.update({ 'cnum' : cNum, 'vnum' : vNum })

	context.update({ 'msg_body' : "Chapter " + cNum + " Verse " + vNum, })

	f1 = Q(chapter=cNum) & Q(number=vNum) & Q(author__name='Original Text')

	verse = Verse.objects.filter(f1)

	context.update({ 'verse' : verse, })

	auths = Verse.objects.filter(chapter=cNum).values('author').distinct()

	authors = []
	for a in auths:
		authors.append(Author.objects.get(pk=a['author']))

	context.update({ 'authors' : authors, })

	f2 = Q(cnum=cNum) & Q(vnum=vNum)

	comments = Comment.objects.filter(f2)

	context.update({ 'comments' : comments, })

	if(cSuccess):
		context.update({ 'messages' : ['Your comment has been posted successfully'], 'cSuccess' : cSuccess, })

	return render_to_response("verse.html", context_instance=context)

def getChapter(request):

	try:
		authorName = request.POST.get('authorName', False)
		chapterNum = request.POST.get('chapterNum', False)
	except:
		raise

	f1 = Q(chapter=chapterNum) & Q(author__name=authorName)

	verses = Verse.objects.filter(f1)

	results = []

	for v in verses:
		results.append({ 'verseNum' : v.number, 'vtext' : v.vtext, 'author' : v.author.name, 'authorid' : v.author.id, 'lang' : v.author.alang.name })

	return HttpResponse(json.dumps(results), mimetype="application/json")

def getVerse(request):
	try:
		authorName = request.POST.get('authorName', False)
		chapterNum = request.POST.get('chapterNum', False)
		verseNum = request.POST.get('verseNum', False)
	except:
		raise

	f1 = Q(chapter=chapterNum) & Q(number=verseNum) & Q(author__name=authorName)

	verses = Verse.objects.filter(f1)

	results = []

	for v in verses:
		results.append({ 'verseNum' : v.number, 'vtext' : v.vtext, 'author' : v.author.name, 'authorid' : v.author.id, 'lang' : v.author.alang.name })

	return HttpResponse(json.dumps(results), mimetype="application/json")
