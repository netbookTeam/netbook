from django.http import HttpResponse
from django.shortcuts import redirect       
from django.contrib.auth.models import User
from .models import UserInfo, Novel

def authenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		else: 
			return view_func(request, *args, **kwargs)

	return wrapper_func

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs): 
        user= request.user._wrapped if hasattr(request.user,'_wrapped') else request.user # get User from request.user
        print("type : ",type(user))
        # u=User.objects.get(pk=request.user.pk)
        # print(u.userinfo)
        if user.userinfo.role==UserInfo.ADMIN:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrapper_function

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('index')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def author_check(view_func):
	def wrapper_function(request, slug, *args, **kwargs): 
		user= request.user._wrapped if hasattr(request.user,'_wrapped') else request.user # get User from request.user
		print("type : ",type(user))
		print("slug in check : ",slug)
        # u=User.objects.get(pk=request.user.pk)
        # print(u.userinfo)
		novel = Novel.objects.get(slug=slug)
		if request.user.username == novel.userinfo.user.username:
			return view_func(request, slug, *args, **kwargs)			
		else:
			return redirect('index')
	return wrapper_function

def author_or_admin(view_func):
    def wrapper_function(request, *args, **kwargs): 
        user= request.user._wrapped if hasattr(request.user,'_wrapped') else request.user # get User from request.user
        print("type : ",type(user))
        # u=User.objects.get(pk=request.user.pk)
        # print(u.userinfo)
        if user.userinfo.role==UserInfo.AUTHOR or user.userinfo.role==UserInfo.ADMIN:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrapper_function

def self_authenticate(view_func):
    def wrapper_func(request, username, *args, **kwargs):
        print("username : ",username)
        user = User.objects.get(pk=request.user.pk)
        if username==user.username:
            return view_func(request, username, *args, **kwargs)
        else:
            return redirect('index')
            
    return wrapper_func
    