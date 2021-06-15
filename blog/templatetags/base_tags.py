from django import template
from ..models import Category


register = template.Library()

@register.simple_tag
def title():
    return 'وبلاگ '


@register.inclusion_tag('partials/category_navbar.html')
def category_navbar():
    return {
        'category':Category.objects.filter(status=True)
    }


@register.inclusion_tag('registration/partials/link.html')
def link(request , link_name , content , classes):
    return {
        'request' : request ,
        'link_name' : link_name ,
        'link': "accounts:{}".format(link_name),
        'content' : content ,
        'classes' : classes ,
    }