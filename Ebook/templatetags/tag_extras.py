from django import template
from Ebook.models import Tag

register = template.Library()

@register.simple_tag
def getTag():
    return list(Tag.objects.all())