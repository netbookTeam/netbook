from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .decorator import authenticated_user,admin_only,unauthenticated_user
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, CreateUserInfoForm

# Create your views here.

def index(request):
    return render(request,"Ebook/main.html",{"name":"index"})

@authenticated_user
def home(request):
    return render(request,"Ebook/main.html",{"name":"home"})

@authenticated_user
@admin_only
def admin(request):
    return render(request,"Ebook/main.html",{"name":"admin"})

@unauthenticated_user
def loginPage(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'Ebook/login.html', context)

@unauthenticated_user
def registerPage(request):

    form1 = CreateUserForm()
    form2 = CreateUserInfoForm()
	
    if request.method == 'POST':
        form1 = CreateUserForm(request.POST)
        form2 = CreateUserInfoForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            info = form2.save()
            info.user = user
            info.save()
            username = form1.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        else:
            print("form1 valid : ",form1.is_valid())
            print("form2 valid : ",form2.is_valid())
            print("form1 error : ",form1.errors) 
            print("form2 error : ",form2.errors) 

    context = {
        'formUser':form1,
        'formInfo':form2,
    }
    return render(request, 'Ebook/register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')