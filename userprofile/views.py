from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse

from authapp.services.notifications import Notification
from mainapp.models import Article, ArticleStatus
from mainapp.forms import ArticleCreationForm


class UserProfileView(View):
    title = 'личный кабинет'
    template_name = 'userprofile/profile.html'

    def get_context_data(self, request):
        statuses = ArticleStatus.objects.all()
        articles_with_status = {}
        for status in statuses:
            articles_with_status[status] = Article.objects.filter(
                author=self.request.user,
                article_status_new=status
            )

        context = {
            'title': self.title,
            'user': self.request.user,
            'creation_form': ArticleCreationForm(),
            'articles': articles_with_status,
        }
        return context

    def post(self, request):
        print('1')
        values = request.POST.getlist('chk')
        print(values)

    def get(self, request):
        return render(request, self.template_name, self.get_context_data(request))


class ArticleCreationView(CreateView):
    """CBV для создание статьи"""
    model = Article
    form_class = ArticleCreationForm
    success_url = reverse_lazy('profile:main')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.article_status_new = ArticleStatus.objects.get(name='Черновик')
        self.object.save()
        return super().form_valid(form)


class ArticleChangeActiveView(View):
    """CBV для активации статьи"""

    def post(self, request, article_pk):
        target_article = get_object_or_404(Article, pk=article_pk)
        target_article.is_active = False if target_article.is_active else True

        if target_article.article_status_new.name == 'В архиве':
            target_article.article_status_new = ArticleStatus.objects.get(name='Черновик')
        else:
            target_article.article_status_new = ArticleStatus.objects.get(name='В архиве')
            notification = Notification(target_article, context='archive')
            notification.send()



        target_article.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SendToModeration(View):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='На модерации')
        article.save()
        notification = Notification(article, context='moderation')
        notification.send()
        return HttpResponseRedirect(reverse('profile:main'))


class ArticleEditView(View):
    """Контроллер для изменения статьи"""
    title = 'Редактирование статьи'
    template_name = 'mainapp/edit_article.html'
    form_class = ArticleCreationForm
    redirect_to = 'profile:main'

    def get(self, request, pk):
        context = {
            'form': self.form_class(instance=Article.objects.get(pk=pk)),
            'article': Article.objects.get(pk=pk)
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article_form = ArticleCreationForm(
            data=request.POST, files=request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            if article.article_status_new == ArticleStatus.objects.get(name='Опубликована'):
                article.article_status_new = ArticleStatus.objects.get(name='На модерации')
                article.save()
                notification = Notification(article, context='moderate_after_edit')
                notification.send()

        return HttpResponseRedirect(reverse(self.redirect_to))


class DraftArticle(View):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='Черновик')
        article.save()
        return HttpResponseRedirect(reverse('profile:main'))
