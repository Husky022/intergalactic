from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from mainapp.models import Article, Comment


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
        return context

def article_page(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comments = Comment.objects.filter(article_id=article_pk)
    context = {
        'page_title': 'Статья',
        'article': article,
        'article_pk': article.hub_id,
        'comments': comments
    }
    return render(request, 'mainapp/article_page.html', context)


class Hub_category(ListView):
    model = Article
    template_name = 'mainapp/hub_category.html'
    context_object_name = 'hub'
    # allow_empty = False # Когда страница не найдена отдавать 404 ошибку

    def get_queryset(self):
        # Фильтр по категории и сортировка "сначала новые"
        return Article.objects.filter(hub__id=self.kwargs['hub_id']).order_by('-add_datatime')

# class Comments(ListView):
#     model = Comment
#     template_name = 'mainapp/comments.html'
#     context_object_name = 'comments'
#
#     def get_queryset(self):
#         # Фильтр по id статьи
#         return Comment.objects.filter(article__id=self.kwargs['article_id'])
