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
    path('search/<slug:slug>/',views.search_tag,name="search_tag"),
    path('my_work/',views.myWork,name="my_work"),
    path('my_work/<slug:slug>/',views.myWorkDetail,name="my_work_detail"),
    path('my_work/<slug:slug>/create',views.createChapter,name="create_chapter"),
    path('my_work/<slug:slug>/<int:chapter_number>/edit',views.editChapter,name="edit_chapter"),
    path('read/<slug:slug>/<int:chapter_number>/',views.read,name="read"),
    path('detail/<slug:slug>/',views.detail,name="detail"),
    path('profile/edit',views.edit_profile,name="edit_profile"),
    path('profile/general',views.profile_general,name="profile_general"),
    path('profile/follow',views.profile_follow,name="profile_follow"),
    path('rate/',views.rate,name="rate"),
    path('follow/',views.follow,name="follow"),
    path('manage/',views.manage,name="user_manage"),
]