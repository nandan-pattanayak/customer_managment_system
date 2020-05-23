from django.shortcuts import redirect
from django.http import HttpResponse


def unauthenticate_user(view_func):
	def decorator(request,*args,**kwargs):
		if request.user.is_authenticated:
			return redirect('/')
		else:
			return view_func(request,*args,**kwargs)
	return decorator



def allow_user(allow=[]):
	def decorator(view_func):
		def wrapper_func(request,*args,**kwargs):
			group=None
			if request.user.groups.exists():
				group=request.user.groups.all()[0].name
			if group in allow:
				return view_func(request,*args,**kwargs)
			else:
				return HttpResponse("you did not have permision to access this page")
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_func(request,*args,**kwargs):
		group=None
		if request.user.groups.exists():
				group=request.user.groups.all()[0].name
		if group == 'admin':
			return view_func(request,*args,**kwargs)
		if group == 'customer':
			return redirect("user")
	return wrapper_func
