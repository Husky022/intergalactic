from django.shortcuts import get_object_or_404, render
from django.views.generic import View, CreateView, ListView, DetailView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse

from mainapp.forms import ArticleCreationForm, CommentForm, SubCommentForm
from mainapp.models import Article, Comment, Likes, SubComment, Hosts, Art_Visits
from mainapp.services.activity.parse import queryset_activity
from mainapp.services.activity.view import Activity
from mainapp.services.commentsparse import comment
from mainapp.models import Article, ArticleStatus, Comment, Likes
from django.views.decorators.csrf import csrf_exempt


class Main(ListView):
    """ CBV Главной страницы """
    template_name = 'mainapp/index.html'
    paginate_by = 5
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        queryset = queryset_activity(self)
        return queryset


class Articles(ListView):
    """ CBV хабов страницы """
    model = Article
    template_name = 'mainapp/articles.html'
    extra_context = {'title': 'Статьи'}
    paginate_by = 5

    def get_queryset(self):
        queryset = queryset_activity(self)
        return queryset


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
        # подсчёт рейтинга (и просмотров):
        visitor_IP = request.get_host()
        print(f'int(kwargs["pk"] = {int(kwargs["pk"])}')
        Hosts.objects.get_or_create(host=visitor_IP)
        self.object = self.get_object()
        for v in Art_Visits.objects.filter(host=Hosts.objects.get(host=visitor_IP).pk):
            if v.article_id == int(kwargs["pk"]):
                break
        else:
            self.object.views += 1
            v = Art_Visits(article=self.object,
                           host=Hosts.objects.get(host=visitor_IP))
            v.save()
        lks = Likes.objects.filter(article_id=int(kwargs["pk"]))
        like_count = lks.filter(status='LK').count()
        dislike_count = lks.filter(status='DZ').count()
        cmnts = Comment.objects.filter(
            article_id=int(kwargs["pk"])).filter(is_active=True)
        comment_count = cmnts.count()
        sub_cmnt_count = 0
        for cmnt in cmnts:
            sub_cmnt_count += SubComment.objects.filter(
                comment=cmnt).filter(is_active=True).count()
        # Окончательная формула рейтинга:
        self.object.rating = dislike_count + self.object.views * 2 + \
            like_count * 3 + comment_count * 4 + sub_cmnt_count * 5
        # print(
        #     f'cmnt: {comment_count}   sub_cmnt: {sub_cmnt_count}   dislike_count {dislike_count}   views {self.object.views}   like_count {like_count}')
        self.object.save()

        return Activity.create("get", self)

    def post(self):
        return Activity.create("post", self)


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
