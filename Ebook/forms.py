from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

from .models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']

class CreateUserInfoForm(ModelForm):
	class Meta:
		model = UserInfo
		fields = ['name' , 'email' , 'phone' , 'address']

class CreateNovelForm(ModelForm):
	class Meta:
		model = Novel
		fields = ['title' , 'description' , 'thumbnail' , 'tags']

class CreateChapterForm(ModelForm):
	class Meta:
		model = Chapter
		fields = ['title' , 'number' , 'content']

class CreateRatingForm(ModelForm):
	class Meta:
		model = Rating
		fields = ['rate']