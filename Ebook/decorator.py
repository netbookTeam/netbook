from django.http import HttpResponse
from django.shortcuts import redirect       
from django.contrib.auth.models import User

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        username=str(request.user)  #triadmin
        u=User.objects.get(username=username)
        print(u.userinfo)
        if u.userinfo.role==1:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper_function