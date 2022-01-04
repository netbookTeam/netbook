from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Novel)
admin.site.register(Tag)
admin.site.register(Chapter)    
admin.site.register(NovelTag)
admin.site.register(Rating)
admin.site.register(Following)