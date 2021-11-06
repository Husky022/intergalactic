import json
from datetime import datetime
from pprint import pp, pprint

from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, request
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from authapp.models import NotificationModel
from authapp.services.notifications import Notification
from mainapp.models import Article, ArticleStatus
from moderation.models import ArticleMessage, Complaint, ComplaintMessage
from .utilities import check_complaints


class ModerationMixin(View):
    """Это проверка, что пользователь является админимстратором или модератором.
    Все классы отнаследованные от него, наследуют эту проверку."""

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class Moderator(ModerationMixin, ListView):
    model = Article
    template_name = 'moderation/moderator.html'
    paginate_by = 5

#    def get_queryset(self):
#        queryset = Article.objects.filter(
#            article_status_new=ArticleStatus.objects.get(name='На модерации'))
#        return queryset # ie-178 Dmitrij

    def get_context_data(self, **kwargs):
        context = super(Moderator, self).get_context_data(**kwargs)
        context['title'] = 'модератор'
        context['objects_list'] = Article.objects.filter(
            article_status_new=ArticleStatus.objects.get(name='На модерации'))
        context['notifications_not_read'] = NotificationModel.objects.filter(is_read=0,
                                                                             recipient=self.request.user.id).count()
        return context


class ModerationArticleView(View):
    template_name = 'moderation/article_page.html'

    def get_context_data(self, pk):
        context = {
            'title': 'Статья',
            'user': self.request.user,
            'article': get_object_or_404(Article, pk=pk),
            'messages': ArticleMessage.objects.filter(article=Article.objects.get(pk=pk)).order_by('-datetime'),
            'notifications_not_read': NotificationModel.objects.filter(is_read=0,
                                                                       recipient=self.request.user.id).count()
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
            notification = Notification(message)
            notification.send()
            result = {
                'author': message.message_from.username,
                'datetime': message.datetime.strftime('%d-%m-%Y %H:%M'),
                'text': message.text
            }
            return JsonResponse(result)


class ApproveArticle(ModerationMixin):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.article_status_new = ArticleStatus.objects.get(
            name='Опубликована')
        article.save()
        notification = Notification(article, context='published')
        notification.send()
        return HttpResponseRedirect(reverse_lazy('moderation:main'))


class RejectArticle(ModerationMixin):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.article_status_new = ArticleStatus.objects.get(
            name='Требует исправления')
        article.save()
        notification = Notification(article, context='rejected')
        notification.send()
        return HttpResponseRedirect(reverse_lazy('moderation:main'))


# class BlockedArticle(ModerationMixin):
#     def get(self, request, pk):
#         article = get_object_or_404(Article, pk=pk)
#         article.article_status_new = ArticleStatus.objects.get(name='Заблокированна')
#         article.is_active = False
#         article.save()
#         return HttpResponseRedirect(reverse_lazy('moderation:main'))


class ModerateComplaints(ModerationMixin, ListView):
    model = Complaint
    template_name = 'moderation/moderate_complaints.html'
    extra_context = {'title': 'Модератор'}
    paginate_by = 5

    def get_queryset(self):
        check_complaints()
        queryset = Complaint.objects.filter(
            is_active=True).order_by('-datetime')
        pprint(queryset)
        return queryset


class ModerationArticleComplaintView(View):
    template_name = 'moderation/article_complaint_page.html'

    def get_context_data(self, pk):
        # article = get_object_or_404(Article, pk=pk)
        article = Complaint.objects.get(pk=pk).article
        complainant = Complaint.objects.get(pk=pk).complainant
        context = {
            'title': 'Статья',
            'user': self.request.user,
            'article': article,
            # 'complainant': Complaint.objects.filter(article=article.pk).last().complainant,
            'complainant': complainant,
            'messages': ComplaintMessage.objects.filter(complaint=pk).order_by('-datetime')
        }
        return context

    def get(self, request, pk):
        article = Complaint.objects.get(pk=pk).article
        # if self.request.user.is_authenticated and (self.request.user == article.author or self.request.user.is_superuser or self.request.user.is_stuff or self.request.user == Complaint.objects.get(article=article).last().complainant):
        if self.request.user.is_authenticated and (self.request.user == article.author or self.request.user.is_superuser or self.request.user == Complaint.objects.filter(article=article).last().complainant):
            return render(request, self.template_name, self.get_context_data(pk))

        return render(request, 'moderation/err_article_on_moderation.html', self.get_context_data(pk))


class RegisterNewComplaintMessage(View):
    def post(self, request):
        if request.is_ajax():
            ajax = json.loads(request.body.decode('utf-8'))
            article = Article.objects.get(pk=ajax.get('article'))
            complaint = Complaint.objects.filter(article=article).last()
            message = ComplaintMessage(
                complaint=complaint,
                article=article,
                message_from=request.user,
                text=ajax.get('text')
            )
            message.save()

            result = {
                'author': message.message_from.username,
                'datetime': message.datetime.strftime('%d-%m-%Y %H:%M'),
                'text': message.text
            }
            return JsonResponse(result)
