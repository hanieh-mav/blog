from django.shortcuts import render , get_object_or_404
from django.views.generic import ListView , DetailView 
from accounts.models import User
from accounts.mixins import AcessAuthor
from django.core.paginator import Paginator
from .models import Article , Category


# Create your views here.
class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 5


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(),slug=slug)


class ArticlePreview(AcessAuthor,DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article,pk=pk)


class CategoryList(ListView):
    paginate_by = 6
    template_name = 'blog/category_list.html'
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(),slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 6
    template_name = 'blog/author_list.html'
    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User,username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context    
        

#FuNcation view
# def home(request,page=1):
#     article_list = Article.objects.published().order_by('publish')
#     paginator = Paginator(article_list,6)
#     article = paginator.get_page(page)
#     context = {
#         'article':article,
#              }
#     return render(request,'blog/index.html',context)


# def detail_article(request,slug):
#     article = get_object_or_404(Article.objects.published(),slug=slug) 
#     context = {
#         'article':article
#     }  
#     return render(request,'blog/detail_article.html',context)


# def category(request,slug,page=1):
#     category = get_object_or_404(Category,slug=slug,status=True)
#     article_list = category.articles.published()
#     pagination = Paginator(article_list,2)
#     article = pagination.get_page(page) 
#     context = {
#         'category':category,
#         'article':article
#     }   
#     return render(request,'blog/category.html',context)