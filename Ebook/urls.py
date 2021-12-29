from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('home/',views.home,name="home"),
    path('adminsite/',views.admin,name="admin"),
    path('login/',views.loginPage,name="login"),
    path('register/',views.registerPage,name="register"),
]