from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.template.loader import render_to_string
from django.views.generic import View, CreateView, ListView, DetailView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from authapp.models import NotificationModel
from mainapp.models import Article, ArticleStatus, VoiceArticle
from mainapp.services.activity.parse import RenderArticle
from mainapp.forms import ArticleCreationForm, CommentForm, SubCommentForm
from .search_filter import ArticleFilter

from .services.activity.comment import CommentSubcomment
from .services.activity.likes import LikeDislike
from .services.activity.other import view_views, rating
from .services.audio import play_text


class Main(ListView):
    """ CBV Главной страницы """
    template_name = 'mainapp/articles.html'
    paginate_by = 5
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        queryset = RenderArticle(self.kwargs).queryset_activity()
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        context['notifications_not_read'] = NotificationModel.objects.filter(is_read=0,
                                                                             recipient=self.request.user.id).count()
        return self.render_to_response(context)


class Articles(ListView):
    """ CBV хабов страницы """
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}
    context_object_name = 'articles'
    ordering = ['add_datetime']
    paginate_by = 5

    def get_queryset(self):
        queryset = RenderArticle(self.kwargs).queryset_activity()
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        context['notifications_not_read'] = NotificationModel.objects.filter(is_read=0,
                                                                             recipient=self.request.user.id).count()
        return self.render_to_response(context)


class ArticlePage(DetailView):
    """CBV одной статьи"""
    template_name = 'mainapp/article_page.html'
    model = Article
    extra_context = {
        'page_title': 'Статья',
        'CommentForm': CommentForm,
        'SubCommentForm': SubCommentForm
    }

    def get(self, request, *args, **kwargs):
        # Добавление и валидация просмотра
        view_views(self)
        # Валидация на добавление или удаление дизлайков или лайков
        if self.request.GET.dict().get("text_comment") or self.request.GET.dict().get("text_subcomment"):
            CommentSubcomment(self.request, self.kwargs, self.request.GET.dict()).add_get_or_post()
        elif self.request.GET.dict().get("com_delete") or self.request.GET.dict().get("sub_com_delete"):
            CommentSubcomment(self.request, self.kwargs, self.request.GET.dict()).delete_get_or_post()
        elif self.request.GET.dict().get("status"):
            LikeDislike(self.request, self.kwargs, ).status_like()
        # Набор контекста
        self.object = self.get_object()
        context = self.get_context_data(object=self.get_object())
        context = CommentSubcomment(self.request, self.kwargs).render_context(context)
        context['likes'] = LikeDislike(self.request, self.kwargs).view_like()
        context["rating"] = rating(self.object)
        context['notifications_not_read'] = NotificationModel.objects.filter(is_read=0,
                                                                             recipient=self.request.user.id).count()
        context['audio'] = VoiceArticle.objects.filter(article=self.object).first()
        if self.request.is_ajax():
            result = render_to_string('mainapp/includes/inc__activity.html', context, request=self.request)
            # Отправка аяксу результата
            return JsonResponse({"result": result})
        # Рендер обычного гет запроса
        return self.render_to_response(context)

    def post(self):
        CommentSubcomment(self.request, self.kwargs, self.request.POST.dict()).add_get_or_post()
        CommentSubcomment(self.request, self.kwargs, self.request.POST.dict()).delete_get_or_post()
        return HttpResponseRedirect(reverse_lazy('article_page', args=(int(self.kwargs["pk"]),)))


class ArticleCreationView(CreateView):
    """CBV для создание статьи"""
    model = Article
    form_class = ArticleCreationForm
    success_url = reverse_lazy('auth:profile')

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
        article_form = ArticleCreationForm(
            data=request.POST, files=request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            if article.article_status_new == ArticleStatus.objects.get(name='Опубликована'):
                article.article_status_new = ArticleStatus.objects.get(name='На модерации')
                article.save()

        return HttpResponseRedirect(reverse(self.redirect_to))


class SendToModeration(View):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='На модерации')
        unique_file = play_text(article)
        VoiceArticle.objects.create(audio_file=f"audio/{unique_file}", article=article)
        article.save()
        return HttpResponseRedirect(reverse('auth:profile'))


class DraftArticle(View):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='Черновик')
        article.save()
        return HttpResponseRedirect(reverse('auth:profile'))


class Search(ListView):
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Поиск'}
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        article = Article.objects.filter(article_status='PB')
        search_filter = ArticleFilter(request.GET, queryset=article)
        article = search_filter.qs
        self.object_list = article
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        context['search_filter'] = search_filter
        context['filter'] = request.GET.dict()
        return render(request, 'mainapp/articles.html', context)


class Sorted(ListView):
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        article = Article.objects.filter(article_status='PB')
        context = self.get_context_data()

        if request.GET.dict().get("sorting_by_date") == 'first_new':
            self.object_list =  article.order_by('-add_datetime')
        else:
            self.object_list = article.order_by('add_datetime')

        return render(request, 'mainapp/articles.html', context)



# class Sorted(ListView):
#     """Поиск статей"""
#     # paginate_by = 5
#     model = Article
#     template_name = 'mainapp/articles.html'
#
#     def get_queryset(self):
#         return Article.objects.filter(name__contains=self.request.GET.get("q", ''))
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["by_date"] = self.request.GET.get("by_date", '')
#         return context