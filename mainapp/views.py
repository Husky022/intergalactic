from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from mainapp.models import Article, Comment, IntergalacticUser
from mainapp.forms import CommentForm


comments_quantity_dict = {id: len(Comment.objects.filter(article_id=id))  for id in range(1000)}

class Main(ListView):
    model = Article
    template_name = 'mainapp/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        context['comments'] = Comment.objects.all()
        context['comments_quantity'] = comments_quantity_dict
        return context


class Articles(ListView):
    template_name = 'mainapp/articles.html'


    def get_queryset(self):
        queryset = Article.objects.all()[:10]
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(comments_quantity_dict)
        context['title'] = 'Статьи'
        context['comments_quantity'] = comments_quantity_dict
        context.update({'CommentForm': CommentForm})
        return context


class ArticlePage(TemplateView):
    template_name = 'mainapp/article_page.html'


    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = self.kwargs.get('article_pk', None)
        print(article_pk)
        article = Article.objects.filter(pk=article_pk).first()
        print(article)
        context['page_title'] = 'Статья'
        context['article'] = article
        context['article_pk'] = article_pk
        context['comments'] = Comment.objects.filter(article_id=article_pk)
        context.update({'CommentForm': CommentForm})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        article_pk = self.kwargs.get('article_pk', None)
        author_pk = request.user.id
        comment = Comment.objects.create(article_id=article_pk, author_id=author_pk, text=self.request.POST.dict()['text_comment'])
        comment.save()
        return HttpResponseRedirect(reverse_lazy('article_page', args=(article_pk,)))


class Hub_category(ListView):
    model = Article
    template_name = 'mainapp/hub_category.html'
    context_object_name = 'hub'
    # allow_empty = False # Когда страница не найдена отдавать 404 ошибку

    def get_queryset(self):
        # Фильтр по категории и сортировка "сначала новые"
        return Article.objects.filter(hub__id=self.kwargs['hub_id']).order_by('-add_datatime')


