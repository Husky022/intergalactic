from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from mainapp.models import Article, Comment
from mainapp.forms import CommentForm


class Main(ListView):
    model = Article
    template_name = 'mainapp/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        context['comments'] = Comment.objects.all()
        return context


class Articles(ListView):
    template_name = 'mainapp/articles.html'


    def get_queryset(self):
        queryset = Article.objects.all()[:10]
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        context['comments_quantity'] = len(Comment.objects.all())
        context.update({'CommentForm': CommentForm})  # передаем форму из forms.py
        return context


def article_page(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    print(article.name)
    comments = Comment.objects.filter(article_id=article_pk)
    comment_form = CommentForm
    context = {
        'page_title': 'Статья',
        'article': article,
        'article_pk': article.hub_id,
        'comments': comments
    }
    return render(request, 'mainapp/article_page.html', context)


class ArticlePage(ListView):
    model = Article
    template_name = 'mainapp/article_page.html'


    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = self.kwargs.get('article_pk', None)
        print(article_pk)
        article = Article.objects.filter(pk=article_pk)
        print(article)
        context['page_title'] = 'Статья'
        context['article'] = article
        context['article_pk'] = article_pk
        context['comment'] = Comment.objects.filter(article_id=article_pk)
        context.update({'CommentForm': CommentForm}) #передаем форму из forms.py
        return self.render_to_response(context)

    # def post(self, request, *args, **kwargs):
    #     context = self.get_context_data()
    #     article_pk = self.kwargs.get('article_pk', None)
    #     formPost = CommentForm(self.request.POST)
    #     if formPost.is_valid():
    #         form_update = formPost.save(commit=False)
    #         form_update.save()
    #         return HttpResponseRedirect(reverse_lazy('article_page', args=(article_pk,)))
    #     else:
    #         print('NotValid')
    #         context['comment'] = Comment.objects.filter(article_id=article_pk)
    #         context.update({'CommentForm': formPost})
    #         return self.render_to_response(context)


class Hub_category(ListView):
    model = Article
    template_name = 'mainapp/hub_category.html'
    context_object_name = 'hub'
    # allow_empty = False # Когда страница не найдена отдавать 404 ошибку

    def get_queryset(self):
        # Фильтр по категории и сортировка "сначала новые"
        return Article.objects.filter(hub__id=self.kwargs['hub_id']).order_by('-add_datatime')


