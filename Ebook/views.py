from django.shortcuts import render
from django.http import HttpResponse
from .decorator import unauthenticated_user,admin_only

# Create your views here.
@unauthenticated_user
def index(request):
    return render(request,"Ebook/main.html",{"name":"index"})

def home(request):
    return render(request,"Ebook/main.html",{"name":"home"})

@admin_only
def admin(request):
    return render(request,"Ebook/main.html",{"name":"admin"})