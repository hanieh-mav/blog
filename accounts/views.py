from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import (FieldMixin , FormValidMixin , AcessAuthor , SuperUserAccessMixin , AuthorsMixin)
from django.views.generic import (ListView , CreateView , UpdateView , DeleteView)
from django.contrib.auth.views import LoginView
from blog.models import Article
from .models import User
from .forms import ProfileForm

class ArticleList(AuthorsMixin,ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)    


class ArticleCreate(AuthorsMixin,FieldMixin,FormValidMixin,CreateView):
    model = Article
    template_name = 'registration/article-create-update.html'    


class ArticleUpdate(AcessAuthor,FieldMixin,FormValidMixin,UpdateView):
    model = Article
    template_name = 'registration/article-create-update.html'       


class ArticleDelete(SuperUserAccessMixin,DeleteView):
    model = Article
    success_url = reverse_lazy('accounts:home') 
    template_name = 'registration/article_delete.html' 


class Profile(LoginRequiredMixin,UpdateView):
    model = User
    template_name = 'registration/profile.html'   
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:home')
    def get_object(self):
        return User.objects.get(pk = self.request.user.pk )

    def get_form_kwargs(self):
        kwargs = super(Profile,self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user
        })    
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy('accounts:home')
        else:
            return reverse_lazy('accounts:profile')          