from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from accounts.models import User
from extentions.utilis import jalali_converter


# Create your models here.
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    parent = models.ForeignKey('self',default=None,null=True,blank=True,verbose_name='زیردسته',on_delete=models.SET_NULL,related_name='children' )
    slug = models.SlugField(max_length=200 , verbose_name='ادرس دسته بندی')
    status = models.BooleanField(default=True,verbose_name='ایا نشان داده شود')
    position = models.IntegerField(verbose_name='پوزیشن')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id','position']

    def __str__(self):
        return self.title   

    objects = CategoryManager()    



class Article(models.Model):
    STATUS_CHOICES = (
        ('d','پیش نویس'),
        ('p','منتشر شده'),
        ('i','در حال بررسی'),
        ('b','برگشت داده شده'),
    )
    title = models.CharField(max_length=100,verbose_name='عنوان مقاله')
    author = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name='articles',verbose_name='نویسنده')
    slug = models.SlugField(max_length=100,unique=True,verbose_name='ادرس مقاله')
    category = models.ManyToManyField(Category,verbose_name='دسته بندی',related_name='articles')
    description = models.TextField(verbose_name='محتوای مقاله')
    thumbnail = models.ImageField(upload_to='article/%Y/%m/%d/',verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now,verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,verbose_name='وضغیت')
    is_special = models.BooleanField(default=False,verbose_name='مقاله ویژه')


    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('accounts:home')


    def jpublish(self):
        return jalali_converter(self.publish)    

    def category_published(self):
        return self.category.filter(status=True) 

    def thumbnail_tag(self):
        return format_html("<img src='{}' width =60 height=50>".format(self.thumbnail.url))

    def category_to_str(self):
        return ' , '.join([category.title for category in self.category.all()])  
    category_to_str.short_description = 'دسته بندی'  

    objects = ArticleManager()       