from django.core.checks import messages
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist

from .models import Comment, Following, Novel, Chapter, Rating, Tag, UserInfo
from .decorator import authenticated_user,admin_only,unauthenticated_user, author_check, author_or_admin, self_authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, CreateUserInfoForm, CreateNovelForm, CreateChapterForm, CreateRatingForm
from django.contrib.auth.models import User
import urllib
from django.core.files import File
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
NOVELS_PER_PAGE=2
NOVELS_IN_TOP_RATES=3
USERS_PER_PAGE=2


def index(request):
    novels=list(Novel.objects.all())
    page_number = request.GET.get('page')
    if page_number is None:
        page_number=1
    # print("page : ",page_number)
    paginator = Paginator(novels, NOVELS_PER_PAGE)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # page = paginator.page(1)
        raise Http404
    except EmptyPage:
        # page = paginator.page(paginator.num_pages)
        raise Http404

    novels = page.object_list
    page_obj = paginator.get_page(page_number)

    tags = list(Tag.objects.all())
    print(type(novels))
    return render(request,"Ebook/index.html",{
        "novels":novels,
        "tags":tags,
        "page_obj":page_obj,
    })

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
            return redirect('index')
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
            info.user = user # relationship one to one 
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
def search(request):
    novels=[]
    keyword=request.GET.get("keyword")
    print("keyword : ",keyword)
    novels=list(Novel.objects.filter(title__contains=keyword))
    print(novels)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number=1
    # print("page : ",page_number)
    paginator = Paginator(novels, NOVELS_PER_PAGE)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # page = paginator.page(1)
        raise Http404
    except EmptyPage:
        # page = paginator.page(paginator.num_pages)
        raise Http404

    novels = page.object_list
    page_obj = paginator.get_page(page_number)
    return render(request,"Ebook/search.html",{
        "novels":novels,
        "page_obj":page_obj,
    })

def search_tag(request, slug=None):
    novels=[]
    tag = Tag.objects.get(slug=slug)
    print("tag : ",tag)
    novels = list(tag.novel_set.all())
    print("novels : ",novels)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number=1
    # print("page : ",page_number)
    paginator = Paginator(novels, NOVELS_PER_PAGE)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # page = paginator.page(1)
        raise Http404
    except EmptyPage:
        # page = paginator.page(paginator.num_pages)
        raise Http404

    novels = page.object_list
    page_obj = paginator.get_page(page_number)
    return render(request,"Ebook/search.html",{
        "novels":novels,
        "page_obj":page_obj,
        "tag" : tag,
    })

@authenticated_user
@author_or_admin
@author_check
def myWorkDetail(request,slug=None):
    novel = get_object_or_404(Novel,slug=slug)
    chapters = list(Chapter.objects.filter(novel=novel))
    return render(request,"Ebook/my_work_detail.html",{"chapters":chapters})

def read(request,slug=None,chapter_number=None):
    if slug is not None and chapter_number is not None:
        novel = get_object_or_404(Novel,slug=slug)
        # chapter_list = list(novel.chapter_set.all())
        cnt = novel.chapter_set.count()
        print("count : ",cnt)
        chapter = get_object_or_404(Chapter,novel=novel,number=chapter_number)
        return render(request,'Ebook/read.html',{
            "novel" : novel,
            "chapter" : chapter,
            "range" : range(1,cnt+1),
            "max_range" : cnt,
        })
    return redirect('index')

@never_cache
def detail(request,slug=None):
    if slug is not None:
        novel = get_object_or_404(Novel,slug=slug)
        form = CreateRatingForm()
        tags = list(novel.tags.all())
        chapters = list(Chapter.objects.filter(novel=novel))
        if len(chapters)>0:
            first_chapter = chapters[0]
        else:
            first_chapter = None
        comments = Comment.objects.filter(novel=novel)

        is_followed = False
        rating = None
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            try:
                following = Following.objects.get(user=user,novel=novel)
            except ObjectDoesNotExist:
                following = None
            if following is not None:
                is_followed = following.is_followed
            
            try:
                rating = Rating.objects.get(user=user,novel=novel)
            except ObjectDoesNotExist:
                rating = None
            if request.method == "POST":
                is_comment = request.POST.get("comment")
                if is_comment is not None:
                    content = request.POST.get("content")
                    comment = Comment()
                    comment.user = user
                    comment.novel = novel
                    comment.content = content
                    comment.save()
                    return redirect('detail',slug=slug)
        
        print("tags : ",tags)
        return render(request,'Ebook/detail.html',{
            "novel" : novel,
            "tags" : tags,
            "chapters" : chapters,
            "form": form,
            "is_followed" : is_followed,
            "comments" : comments,
            "first_chapter" : first_chapter,
            "rating" : rating,
        })
    return redirect('index')

@authenticated_user
@author_or_admin
def myWork(request, slug=None):
    user = User.objects.get(pk=request.user.pk)
    novels = list(Novel.objects.filter(userinfo=user.userinfo))
    print("novels : ",novels)
    return render(request,'Ebook/my_work.html',{"novels":novels})

@authenticated_user
@author_or_admin
def createNovel(request):
    form = CreateNovelForm()
    if request.method == "POST":
        form = CreateNovelForm(request.POST, request.FILES)
        if form.is_valid():
            # user= request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
            u=User.objects.get(pk=request.user.pk)
            userInfo=u.userinfo
            novel=form.save()
            novel.userinfo=userInfo
            novel.save()
            print(novel.tags.all())
        return redirect('login')
    context={
        "form":form,
    }
    return render(request, "Ebook/create_novel.html",context)


@authenticated_user
@author_or_admin
@cache_control(no_cache=True, must_revalidate=True)
def createChapter(request, slug=None):
    novel = get_object_or_404(Novel,slug=slug)
    form = CreateChapterForm()
    if request.method == "POST":
        form = CreateChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save()
            chapter.novel = novel
            chapter.save()
            return redirect('my_work_detail',slug=slug)
    context={
        "form":form
    }
    return render(request,"Ebook/create_chapter.html",context)

@cache_control(no_cache=True, must_revalidate=True)
@authenticated_user
@author_or_admin
@author_check
def editChapter(request, slug=None, chapter_number=None):
    novel = get_object_or_404(Novel,slug=slug)
    # novel = Novel.objects.get(slug=slug)
    chapter = get_object_or_404(Chapter,novel=novel,number=chapter_number)
    # chapter = Chapter.objects.get(novel=novel,number=chapter_number)
    # form = CreateChapterForm()
    if request.method == "POST": 
        is_delete = request.POST.get("delete")
        if is_delete is not None: 
            chapter.delete()
            return redirect('my_work_detail',slug=slug)
        else:
            form = CreateChapterForm(request.POST,instance=chapter)
            if form.is_valid():
                form.save()
                # return redirect('my_work_detail',slug=slug)
    
    # if slug is not None and chapter_number is not None:
        # novel = Novel.objects.get(slug=slug)
    form = CreateChapterForm(instance=chapter)
    context={
        "form":form
    }
    return render(request,"Ebook/edit_chapter.html",context)

@authenticated_user
@self_authenticate
def profile_details(request):
    # print('view profile')
    username = request.user.username
    user = User.objects.get(username=username)
    info = UserInfo.objects.get(user=user)
    if request.method == "POST": 
        form = CreateUserInfoForm(request.POST,instance=info)
        print('111')
        print(form.data)
        if form.is_valid():
            print('ok')
            form.save()
            return redirect('profile_details')
    
    form = CreateUserInfoForm(instance=info)
    # print(form)
    context={
        "form":form
    }
    # print('view form')
    return render(request,"Ebook/profile_details.html",context)

@never_cache
@authenticated_user
def rate(request):
    if request.method == "POST":
        slug = request.POST.get("novel")
        novel = Novel.objects.get(slug=slug)
        if novel is not None:
            user = User.objects.get(pk=request.user.pk)
            print("#type : ",type(user))
            print("#name : ",user.userinfo.name)
            ratingForm = CreateRatingForm(request.POST)
            rating = ratingForm.save(commit=False)
            rating.novel = novel
            rating.user = user
            rating.save()

            prev_number=novel.number_rating
            sum_rate=prev_number*novel.avg_rate
            sum_rate+=1.0*rating.rate
            novel.number_rating+=1

            novel.avg_rate=sum_rate/novel.number_rating
            novel.save()

            return redirect('detail',slug=novel.slug)
    return redirect('index')

@authenticated_user
def profile_general(request):
    user = User.objects.get(pk=request.user.pk)
    userinfo = UserInfo.objects.get(user=user)
    return render(request,"Ebook/profile_general.html",{"userinfo":userinfo})

@authenticated_user
def follow(request):
    if request.method == "POST":
        print("in POST")
        slug = request.POST.get("slug")
        if slug is not None:
            novel = get_object_or_404(Novel,slug=slug)
            user = User.objects.get(pk=request.user.pk)
            try:
                following = Following.objects.get(user=user,novel=novel)
            except ObjectDoesNotExist:
                following = None
            
            if following is None:
                following = Following()
                following.user = user
                following.novel = novel
            following.is_followed = not following.is_followed
            following.save()
            return redirect('detail',slug=slug)
    return redirect('index')

@authenticated_user
def profile_follow(request):
    user = User.objects.get(pk=request.user.pk)
    followings = list(Following.objects.filter(user=user,is_followed=True))
    novels = []
    for following in followings:
        novels.append(following.novel)
    print("#### novels : ",novels)
    return render(request,"Ebook/profile_follow.html",{"novels":novels})
    # return render(request,"Ebook/profile_follow.html")

@authenticated_user
def profile_change_pass(request):
    return render(request,"Ebook/profile_change_pass.html")

def tag_list(request):
    tag_list = list(Tag.objects.all())
    context={"tag_list" : tag_list}
    return context

def top_rates_novel_list(request):
    novel_list = list(Novel.objects.order_by('-avg_rate'))[:NOVELS_IN_TOP_RATES]
    context={"novel_list" : novel_list}
    return context

@admin_only
def manage(request):
    name = request.GET.get('name')
    if name is not None:
        userinfos=list(UserInfo.objects.filter(name=name))
    else:
        userinfos=list(UserInfo.objects.all())
    page_number = request.GET.get('page')
    if page_number is None:
        page_number=1
    # print("page : ",page_number)
    paginator = Paginator(userinfos, USERS_PER_PAGE)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # page = paginator.page(1)
        raise Http404
    except EmptyPage:
        # page = paginator.page(paginator.num_pages)
        raise Http404

    userinfos = page.object_list
    page_obj = paginator.get_page(page_number)
    return render(request,"Ebook/user_manage.html",{
        "userinfos" : userinfos,
        "page_obj" : page_obj,
    })