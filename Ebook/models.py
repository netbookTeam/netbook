from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.template.defaultfilters import slugify
from django.urls import reverse

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
    slug = models.SlugField(null=False)
    description = models.TextField()
    thumbnail = models.ImageField(default="images/placeholder.png", null=True, blank=True,upload_to="images/")
    userinfo = ForeignKey(UserInfo,null=True, blank=True,on_delete=models.CASCADE)
    tags = ManyToManyField(Tag)

    def __str__(self):    
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('detail',kwargs={'slug':self.slug})
    
    def get_absolute_url_write_chapters(self):
        return reverse('my_work_detail',kwargs={'slug':self.slug})
    




class Chapter(models.Model):
    novel = ForeignKey(Novel,null=True, blank=True, on_delete=models.CASCADE)
    number = IntegerField()
    content = models.TextField()
    title = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.novel.title)+"_"+str(self.number)
    
    def get_absolute_url(self):
        slug = self.novel.slug
        return reverse('read',kwargs={'slug':slug,'chapter_number':self.number})
    
    def get_edit_url(self):
        slug = self.novel.slug
        return reverse('edit_chapter',kwargs={'slug':slug,'chapter_number':self.number})
    

class NovelTag(models.Model):
    novel = ForeignKey(Novel,null=True, blank=True,on_delete=models.CASCADE)
    tag = ForeignKey(Tag,null=True, blank=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.novel.title)+" "+str(self.tag.name)