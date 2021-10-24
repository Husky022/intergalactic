from django.shortcuts import get_object_or_404, render
from django.views.generic import View, CreateView, ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from mainapp.forms import ArticleCreationForm, CommentForm, SubCommentForm
from mainapp.models import Article
from mainapp.services.activity.parse import queryset_activity
from mainapp.services.activity.view import Activity


class Main(ListView):
    template_name = 'mainapp/index.html'
    paginate_by = 5
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        queryset = queryset_activity(self)
        return queryset


class Articles(ListView):
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}
    paginate_by = 5

    def get_queryset(self):
        queryset = queryset_activity(self)
        return queryset


class ArticlePage(DetailView):
    template_name = 'mainapp/article_page.html'
    model = Article
    extra_context = {
        'page_title': 'Статья',
        'CommentForm': CommentForm,
        'SubCommentForm': SubCommentForm
    }

    def get(self, request, *args, **kwargs):
        return Activity.create("get", self)

    def post(self):
        return Activity.create("post", self)


class ArticleCreationView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    success_url = reverse_lazy('auth:profile')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleChangeActiveView(View):

    def post(self, request, article_pk):
        target_article = get_object_or_404(Article, pk=article_pk)
        target_article.is_active = False if target_article.is_active else True
        target_article.article_status = 'AR' if target_article.article_status != 'AR' else 'PB'
        target_article.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ArticleEditView(View):
    """Контроллер для изменения статьи"""
    title = 'Редактирование статьи'
    template_name = 'mainapp/edit_article.html'
    form_class = ArticleCreationForm
    redirect_to = 'auth:profile'

    def get(self, request, pk):
        context = {
            'form': self.form_class(instance=Article.objects.get(pk=pk)),
            'article': Article.objects.get(pk=pk)
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article_form = ArticleCreationForm(data=request.POST, files=request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()

        return HttpResponseRedirect(reverse(self.redirect_to))
