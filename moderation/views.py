import json

from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from mainapp.models import Article, ArticleStatus
from moderation.models import ArticleMessage


class ModerationMixin(View):
    """Это проверка, что пользователь является админимстратором или модератором.
    Все классы отнаследованные от него, наследуют эту проверку."""

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class Moderator(ModerationMixin, ListView):
    model = Article
    template_name = 'moderation/moderator.html'
    extra_context = {'title': 'Модератор'}
    paginate_by = 5

    def get_queryset(self):
        queryset = Article.objects.filter(article_status_new=ArticleStatus.objects.get(name='На модерации'))
        return queryset


class ModerationArticleView(View):
    template_name = 'moderation/article_page.html'

    def get_context_data(self, pk):
        context = {
            'title': 'Статья',
            'user': self.request.user,
            'article': get_object_or_404(Article, pk=pk),
            'messages': ArticleMessage.objects.filter(article=Article.objects.get(pk=pk)).order_by('-datetime')
        }
        return context

    def get(self, request, pk):
        if self.request.user.is_authenticated and (self.request.user == Article.objects.get(
                pk=pk).author or self.request.user.is_superuser or self.request.user.is_stuff):
            return render(request, self.template_name, self.get_context_data(pk))

        return render(request, 'moderation/err_article_on_moderation.html', self.get_context_data(pk))


class RegisterNewMessage(View):
    def post(self, request):
        if request.is_ajax():
            ajax = json.loads(request.body.decode('utf-8'))
            message = ArticleMessage(
                article=Article.objects.get(pk=ajax.get('article')),
                message_from=request.user,
                text=ajax.get('text')
            )
            message.save()
            print(type(message.datetime))
            result = {
                'author': message.message_from.username,
                'datetime': message.datetime.strftime('%d-%m-%Y %H:%M'),
                'text': message.text
            }
            return JsonResponse(result)


class ApproveArticle(ModerationMixin):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='Опубликована')
        article.save()
        return HttpResponseRedirect(reverse_lazy('moderation:main'))


class RejectArticle(ModerationMixin):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='Требует исправления')
        article.save()
        return HttpResponseRedirect(reverse_lazy('moderation:main'))


class BlockedArticle(ModerationMixin):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.article_status_new = ArticleStatus.objects.get(name='Заблокированна')
        article.is_active = False
        article.save()
        return HttpResponseRedirect(reverse_lazy('moderation:main'))
