from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponse
from django.template.context import RequestContext

def viewHome(request):
	context = RequestContext(request)
	return render_to_response("home.html", context_instance=context)

def info(request):
	context = RequestContext(request)
	context.update({ 'msg_body' : "", })
	return render_to_response("info.html", context_instance=context)
