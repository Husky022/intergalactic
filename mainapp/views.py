from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.template import loader
from mainapp.forms import ArticleCreationForm, CommentForm
from mainapp.comments import CommentAction
from mainapp.models import Article, Comment, Likes
from django.views.decorators.csrf import csrf_exempt


class Main(ListView):
    template_name = 'mainapp/index.html'
    paginate_by = 5
    extra_context = {
        'title': 'Статьи',
        'comments': Comment.objects.all(),
        'like_status': 'эээээ',
    }

    def get_queryset(self):
        queryset = CommentAction.create("main")
        return queryset


class Articles(ListView):
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}
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
        like_items_article = Likes.objects.filter(article_id=int(kwargs["pk"]))
        user_like = like_items_article.filter(user_id=request.user.pk)
        user_like_status = None
        like_count = like_items_article.filter(like_status=True).count()
        if not user_like:
            user_like_status = False
        elif user_like.filter(like_status=False):
            user_like_status = False
        else:
            user_like_status = True

        context = CommentAction.create("article_page_get", self)
        context.update(user_like_status=user_like_status, like_count=like_count)

        if request.is_ajax():
            CommentAction.create("article_page_ajax", self)
            result = render_to_string(
                'mainapp/includes/inc__comment.html', context)
            return JsonResponse({'result': result})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        CommentAction.create("article_page_post", self)
        return HttpResponseRedirect(reverse_lazy('article_page', args=(int(kwargs["pk"]),)))


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
        # Пока сделал, что все статьи из архива - попадают на модерацию
        # Надо будет обдумать более гибкую логику
        target_article.article_status = 'AR' if target_article.article_status != 'AR' else 'PB'
        target_article.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ArticleEditView(UpdateView):
    """Контроллер для изменения товара"""
    model = Article
    form_class = ArticleCreationForm
    success_url = reverse_lazy('auth:profile')

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


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
