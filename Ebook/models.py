from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField

# Create your models here.

class UserInfo(models.Model):
    ADMIN=1
    AUTHOR=2
    CUSTOMER=3

    ROLE_CHOICES=(
        (ADMIN,'admin'),
        (AUTHOR,'author'),
        (CUSTOMER,'customer'),
    )

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,blank=True,null=True,default=CUSTOMER)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
 
    def __str__(self):
        return self.name

class Novel(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=400, null=True)
    thumbnail = models.ImageField(default="placeholder.png", null=True, blank=True,upload_to="images/")
    userinfo = ForeignKey(UserInfo,null=True, blank=True,on_delete=models.CASCADE)
    tags = ManyToManyField(Tag)
    def __str__(self):    
        return self.title




class Chapter(models.Model):
    novel = ForeignKey(Novel,null=True, blank=True, on_delete=models.CASCADE)
    number = IntegerField()
    content = models.CharField(max_length=1000, null=True)
    

class NovelTag(models.Model):
    novel = ForeignKey(Novel,null=True, blank=True,on_delete=models.CASCADE)
    tag = ForeignKey(Tag,null=True, blank=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.novel.title)+" "+str(self.tag.name)