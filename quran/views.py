from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponse
from django.template.context import RequestContext

def viewHome(request):
	context = RequestContext(request)
	return render_to_response("base.html", context_instance=context)

