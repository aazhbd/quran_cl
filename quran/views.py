"""
 The Holy Quran
 @author        Abdullah Al Zakir Hossain, Email: aazhbd@yahoo.com
 @copyright     Copyright (c)2009-2016 ArticulateLogic Labs
"""
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

from django.template.context import RequestContext
from django.db.models import Q,Count, Min, Max, Sum
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
from quran.models import *
import unicodedata
import json


def viewHome(request):
	context = RequestContext(request)
	context.update({ 'msg_body' : "The Holy Quran", })
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
			try:
				existing = User.objects.get(email=email)
			except:
				existing = None

			if existing is not None:
				context.update({ 'msg_body' : "The sign up information were invalid, already exists " + str(email), })
				return render_to_response("signup.html", context_instance=context)
			else:
				user = User.objects.create_user(email, email, upass)
				user.first_name = name
				user.save()
				context.update({ 'msg_body' : "Congratulations, the signup was successful, You can now login to share your expertise or ask questions on any verse to get answers from Scholars and Enthusiasts", })
		else:
			context.update({ 'msg_body' : "The sign up information were invalid. " + str(email), })
			return render_to_response("signup.html", context_instance=context)

	context.update({ 'msg_body' : "Login", })
	return render_to_response("login.html", context_instance=context)

def viewDiscuss(request):
	context = RequestContext(request)

	comments = Comment.objects.filter(enabled=True).order_by('-date_published')
	context.update({ 'comments' : comments, })

	if request.method == "POST":
		uemail = request.POST.get('email', None).strip()
		password = request.POST.get('password', None).strip()

		try:
			user = User.objects.get(email=uemail)
		except:
			user = None

		if user is not None and user.check_password(password):
			if user.is_active:
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				login(request, user)
				context.update({ 'msg_body' : "Login is successful.", })
			else:
				context.update({ 'msg_body' : "The account is currently inactive, contact administrator.", })
		else:
			context.update({ 'msg_body' : "The username and password were incorrect.", })
			return render_to_response("login.html", context_instance=context)

	context.update({ 'msg_body' : "Recent Discussions", })
	return render_to_response("discuss.html", context_instance=context)

def viewLogout(request):
	context = RequestContext(request)
	logout(request)
	context.update({ 'msg_body' : "You have been logged out.", })
	return render_to_response("login.html", context_instance=context)

def viewSignup(request):
	context = RequestContext(request)
	context.update({ 'msg_body' : "Signup", })
	return render_to_response("signup.html", context_instance=context)

def viewChapter(request, **Args):
	context = RequestContext(request)

	chapterNum = str(Args.get('chap')).strip('/')
	cNum = int(chapterNum)
	context.update({ 'cnum' : cNum, })

	try:
		chName = Chapter.objects.get(pk=cNum)
		context.update({ 'msg_body' : "Verses of the chapter " + chapterNum + ": " + chName.transliteration + " " + chName.arabic_name + " (" + chName.english_name + ")", })
	except:
		context.update({ 'msg_body' : "Invalid chapter number", })

	v = Q(chapter=cNum) & Q(author__name='Original Text')
	full_chap = Verse.objects.filter(v).order_by('number')

	for content in full_chap:
		content.vtext = unicodedata.normalize('NFC', content.vtext)

	context.update({ 'full_chap' : full_chap, })

	auths = Verse.objects.filter(chapter=cNum).values('author').distinct()
	authors = []
	for a in auths:
		authors.append(Author.objects.get(pk=a['author']))

	context.update({ 'authors' : authors, })

	return render_to_response("chapter.html", context_instance=context)

def viewVerse(request, **Args):
	context = RequestContext(request)
	c_success = None

	chapterNum = str(Args.get('chap')).strip('/')
	verseNum = str(Args.get('verse')).strip('/')
	cNum = str(chapterNum)
	vNum = str(verseNum)

	if request.method=="POST":
		ctext = request.POST.get('comment', "")
		comment_type = request.POST.get('comment_type', "")
		cuser = request.user
		captcha_val = request.POST.get('g-recaptcha-response', "")

		if ctext != "" and comment_type != "" and captcha_val != "":
			try:
				c = Comment(user=cuser, vnum=vNum, cnum=cNum, ctext=ctext, comment_type=comment_type)
				c.save()
				context.update({ 'messages' : ['Your comment has been posted successfully'], 'cSuccess' : c_success, })
			except:
				context.update({ 'messages' : ["Invalid request, comment couldn't be saved" ], 'cSuccess' : c_success, })
				raise
		else:
			context.update({ 'messages' : ["Invalid request, comment couldn't be saved" ], 'cSuccess' : c_success, })

	context.update({'cnum': cNum, 'vnum': vNum})

	try:
		chName = Chapter.objects.get(pk=cNum)
		context.update({'msg_body': "Verse "  + vNum + " of the chapter " + cNum + " : " + chName.transliteration + " " + chName.arabic_name + " (" + chName.english_name + ")", })
	except:
		context.update({'msg_body': "Chapter " + cNum + " Verse " + vNum, })

	verse = Verse.objects.filter(Q(chapter=cNum) & Q(number=vNum) & Q(author__name='Original Text'))

	for v in verse:
		v.vtext = unicodedata.normalize('NFC', v.vtext)

	context.update({ 'verse' : verse, })

	auths = Verse.objects.filter(chapter=cNum).values('author').distinct()

	authors = []
	for a in auths:
		authors.append(Author.objects.get(pk=a['author']))

	context.update({ 'authors' : authors, })

	comments = Comment.objects.filter(Q(cnum=cNum) & Q(vnum=vNum) & Q(enabled=True))
	context.update({ 'comments' : comments, })

	cdetail = Chapter.objects.get(pk=chapterNum)
	if cdetail.total_verses:
		total_verse = cdetail.total_verses

		pnext = False
		if int(verseNum) < int(total_verse):
			pnext = True

		pprevious = False
		if int(verseNum) > 1:
			pprevious = True

		context.update({'pnext': pnext, 'pprevious': pprevious, })
	else:
		context.update({'pnext': False, 'pprevious': False, })

	return render_to_response("verse.html", context_instance=context)


def viewSearch(request, **Args):
	context = RequestContext(request)
	try:
		search = request.POST.get('search', Args.get('search'))
	except:
		search = ""

	if search == None:
		search = ""
	search = search.strip()

	try:
		page = str(Args.get('page', 1)).strip('/')
	except:
		page = 1

	pageNum = int(page)
	pageSize = 40
	titleresult = []
	verseresult = []
	commentresult = []

	if search and search != "":
		titlesearch = Q(english_name__icontains=search) | Q(arabic_name__icontains=search) | Q(transliteration__icontains=search)
		versesearch = Q(vtext__icontains=search)
		commentsearch = Q(ctext_icontains=search)
		try:
			titleresult = Paginator(Chapter.objects.filter(titlesearch), pageSize).page(pageNum)
		except:
			titleresult = []

		try:
			verseresult = Paginator(Verse.objects.filter(versesearch), pageSize).page(pageNum)
		except:
			verseresult = []

		try:
			commentresult = Paginator(Comment.objects.filter(commentsearch), pageSize).page(pageNum)
		except:
			commentresult = []

	totalentries = sum(getattr(x, 'paginator', Paginator([], 0)).count for x in [titleresult, verseresult, commentresult])
	totalpages = int(totalentries / pageSize)

	context.update({
		'titleresult' : titleresult,
		'verseresult' : verseresult,
		'commentresult' : commentresult,
		'searchkey' : search,
		'pageNum' : pageNum,
		'pageSize': pageSize,
		'totalresult' : totalentries,
		'totalpages' : totalpages
	})

	return render_to_response("search.html", context_instance=context)

def getChapter(request):
	try:
		authorName = request.POST.get('authorName', False)
		chapterNum = request.POST.get('chapterNum', False)
	except:
		raise

	verses = Verse.objects.filter(Q(chapter=chapterNum) & Q(author__name=authorName))

	results = []
	for v in verses:
		results.append({
			'verseNum' : v.number,
			'vtext' : unicodedata.normalize('NFC', v.vtext),
			'author' : v.author.name,
			'authorid' : v.author.id,
			'lang' : v.author.alang.name
		})

	return HttpResponse(json.dumps(results), content_type="application/json")

def getVerse(request):
	try:
		authorName = request.POST.get('authorName', False)
		chapterNum = request.POST.get('chapterNum', False)
		verseNum = request.POST.get('verseNum', False)
	except:
		raise

	verses = Verse.objects.filter(Q(chapter=chapterNum) & Q(number=verseNum) & Q(author__name=authorName))

	results = []
	for v in verses:
		results.append({
			'verseNum' : v.number,
			'vtext' : unicodedata.normalize('NFC', v.vtext),
			'author' : v.author.name,
			'authorid' : v.author.id,
			'lang' : v.author.alang.name
		})

	return HttpResponse(json.dumps(results), content_type="application/json")
