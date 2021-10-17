from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from mainapp.comments import CommentAction
from mainapp.models import Article, Comment
from mainapp.forms import CommentForm


class Main(ListView):
    template_name = 'mainapp/index.html'
    extra_context = {
        'title': 'Статьи',
        'comments': Comment.objects.all(),
    }
    paginate_by = 5

    def get_queryset(self):
        queryset = CommentAction.create("main")
        return queryset


class Articles(ListView):
    template_name = 'mainapp/articles.html'
    extra_context = {
        'title': 'Статьи'
    }
    paginate_by = 5

    def get_queryset(self):
        queryset = CommentAction.create("article", self)
        return queryset


class ArticlePage(DetailView):
    template_name = 'mainapp/article_page.html'
    model = Article
    extra_context = {
        'page_title': 'Статья',
        'CommentForm': CommentForm,
    }

    def get(self, request, *args, **kwargs):
        context = CommentAction.create("article_page_get", self)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        CommentAction.create("article_page_post", self)
        return HttpResponseRedirect(reverse_lazy('article_page', args=(int(kwargs["pk"]),)))
