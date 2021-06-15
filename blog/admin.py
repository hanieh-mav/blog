from django.contrib import admin
from .models import Article , Category
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','slug','parent','status',)
    list_display_links = ('title',)
    list_editable = ('status',)
    search_fields = ('title','slug')
    list_filter = (['status'])
    prepopulated_fields = {
        'slug':('title',)
    }
    list_per_page = 15
    



def make_published(ModelAdmin,request,queryset):
    queryset.update(status = 'p')
make_published.short_description = "Mark selected articles as published"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','thumbnail_tag','author','slug','status','is_special','jpublish','category_to_str')
    list_display_links = ('title',)
    search_fields = ('title','description')
    list_filter = ('status','publish','author')
    prepopulated_fields = {
        'slug':('title',)
    }
    list_per_page = 15

    

    actions = [make_published]

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)