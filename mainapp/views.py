from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.template import loader

from mainapp.forms import ArticleCreationForm, CommentForm, SubCommentForm
from mainapp.services.commentsparse import comment
from mainapp.models import Article, ArticleStatus, Comment, Likes
from django.views.decorators.csrf import csrf_exempt

from mainapp.services.commentsview import CommentAction


class Main(ListView):
    template_name = 'mainapp/index.html'
    paginate_by = 5
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        queryset = comment(self)
        return queryset


class Articles(ListView):
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}
    paginate_by = 5

    def get_queryset(self):
        queryset = comment(self)
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
        like_items_article = Likes.objects.filter(article_id=int(kwargs["pk"]))
        user_like = like_items_article.filter(user_id=request.user.pk)
        like_count = like_items_article.filter(like_status=True).count()
        if not user_like:
            user_like_status = False
        elif user_like.filter(like_status=False):
            user_like_status = False
        else:
            user_like_status = True

        context = CommentAction.create("comment_get", self, user_like_status, like_count)
        if request.is_ajax():
            result = CommentAction.create("comment_ajax", self, user_like_status, like_count, self.request.GET.dict())
            return JsonResponse({'result': result})
        return self.render_to_response(context)

    def post(self, **kwargs):
        CommentAction.create("comment_post", self, self.request.POST.dict())
        return HttpResponseRedirect(reverse_lazy('article_page', args=(int(kwargs["pk"]),)))


class ArticleCreationView(CreateView):
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
        article_form = ArticleCreationForm(data=request.POST, files=request.FILES, instance=article)
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
        article.save()
        return HttpResponseRedirect(reverse('auth:profile'))


class DraftArticle(View):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='Черновик')
        article.save()
        return HttpResponseRedirect(reverse('auth:profile'))


# class Like(DetailView):
#     template_name = 'mainapp/article_page.html'
#     model = Likes
#     extra_context = {
#         'LikeForm': LikeForm,
#     }
#
#     def get(self, request, *args, **kwargs):
#         context = CommentAction.create("like_get", self)
#         if request.is_ajax():
#             CommentAction.create("like_ajax", self)
#             result = render_to_string(
#                 'mainapp/includes/inc__like.html', context)
#             return JsonResponse({'result': result})
#         return self.render_to_response(context)
#
#     def post(self, request, *args, **kwargs):
#         CommentAction.create("like_post", self)
#         return HttpResponseRedirect(reverse_lazy('article_page', args=(int(kwargs["pk"]),)))

# @login_required
@csrf_exempt
def set_like(request, article_pk):
    like_items_article = Likes.objects.filter(article_id=article_pk)
    user_like = like_items_article.filter(user_id=request.user.pk)
    user_like_first = user_like.first()
    like_count = like_items_article.filter(like_status=True).count()
    context = {
        'like_items_article': like_items_article,
    }
    if request.is_ajax():
        if not user_like:
            Likes.objects.create(
                article_id=article_pk,
                user_id=request.user.pk,
                like_status=True
            )
            like_list = loader.render_to_string(
                'mainapp/includes/inc__like.html',
                context=context,
                request=request,
            )
            like_count += 1
            return JsonResponse({
                'status': 'ok',
                'like_status': True,
                'like_list': like_list,
                'like_count': like_count,
            })

        elif user_like.filter(like_status=False):

            like_list = loader.render_to_string(
                'mainapp/includes/inc__like.html',
                context=context,
                request=request,
            )
            user_like_first.like_status = True
            user_like_first.save()
            like_count += 1
            return JsonResponse({
                'status': 'ok',
                'like_status': True,
                'like_list': like_list,
                'like_count': like_count,
            })

        else:
            like_list = loader.render_to_string(
                'mainapp/includes/inc__like.html',
                context=context,
                request=request,
            )
            user_like_first.like_status = False
            user_like_first.save()
            like_count -= 1
            return JsonResponse({
                'status': 'ok',
                'like_status': False,
                'like_list': like_list,
                'like_count': like_count,
            })
