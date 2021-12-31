from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('home/',views.home,name="home"),
    path('adminsite/',views.admin,name="admin"),
    path('login/',views.loginPage,name="login"),
    path('register/',views.registerPage,name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('create_novel/',views.createNovel,name="create_novel"),
    path('search/',views.search,name="search"),
    path('my_work/',views.myWork,name="my_work"),
    path('my_work/<slug:slug>/',views.myWorkDetail,name="my_work_detail"),
    path('my_work/<slug:slug>/create',views.createChapter,name="create_chapter"),
    path('read/<slug:slug>/<int:chapter_number>/',views.read,name="read"),
    path('detail/<slug:slug>/',views.detail,name="detail"),
]