from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('home/',views.home,name="home"),
    path('adminsite/',views.admin,name="admin"),
]