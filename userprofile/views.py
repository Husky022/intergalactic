import json
import locale
import pytz

from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import View, CreateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse

from authapp.models import IntergalacticUser, NotificationModel
from authapp.services.notifications import Notification
from mainapp.models import Article, ArticleStatus
from mainapp.forms import ArticleCreationForm
from mainapp.services.audio import play_text
from moneyapp.models import UserBalance
from moneyapp.models import Transaction
from userprofile.models import Message, Chat, NewMessage

from time import sleep
from datetime import timedelta


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
            'notifications_not_read': NotificationModel.objects.filter(is_read=0,
                                                                         recipient=self.request.user.id).count(),
            'balance': round(UserBalance.objects.filter(user_id=self.request.user.id).first().amount,2),
            'transactions_not_read': Transaction.objects.filter(is_read=False, status='CREATED'),
            'transactions_not_read_count': Transaction.objects.filter(is_read=False, status='CREATED').count(),
        }
        return context

    def post(self, request):
        data = request.POST
        send_to_email_value = True if data.dict()['value_checkbox'] == "true" else False
        current_user = IntergalacticUser.objects.filter(id=request.user.id).first()
        current_user.send_to_email = send_to_email_value
        current_user.save()
        return JsonResponse({'status': 'success'})

    def get(self, request):
        if not UserBalance.objects.filter(user_id=request.user.id):
            new_balance = UserBalance.objects.create(user_id=request.user.id)
            new_balance.save()
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
        if request.user.rating_author >= 7:
            article.article_status_new = ArticleStatus.objects.get(name='Опубликована')
            notification = Notification(article, context='published')
            notification.send()
        article.save()
        play_text(pk)
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
            'article': Article.objects.get(pk=pk),
            'notifications_not_read': NotificationModel.objects.filter(is_read=0,
                                                                       recipient=self.request.user.id).count()
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


class OtherUserProfile(View):
    template_name = 'userprofile/other_user.html'
    
    def get(self, request, pk):
        if request.user == IntergalacticUser.objects.get(pk=pk):
            return HttpResponseRedirect(reverse('profile:main'))

        context = {
            'target_user': get_object_or_404(IntergalacticUser, pk=pk),
            'articles': Article.objects.filter(
                author=IntergalacticUser.objects.get(pk=pk),
                article_status_new=ArticleStatus.objects.get(name='Опубликована')
            )
        }
        return render(request, self.template_name, context)


class CorrespondenceView(View):

    def get_context_data(self, request):
        chats = self.get_chats(request)

        members = []
        context = {
            'chats': chats
        }
        return context

    def get(self, request):
        return render(request, 'userprofile/correspondence.html', context=self.get_context_data(request))

    @staticmethod
    def get_chats(request):
        chats = Chat.objects.filter(user=request.user)
        members_and_last_messages = []
        for chat in chats:
            for user in chat.user.all():
                if user != request.user:
                    members_and_last_messages.append({
                        'chat_item': chat,
                        'member': user,
                        'last_message': Message.objects.filter(chat=chat).last(),
                    })

        return members_and_last_messages


class Messages(View):
    def get(self, request, pk):
        """Получить все сообщения чата и отрендерить их"""
        if request.is_ajax():
            chat = Chat.objects.get(pk=pk)
            context = {'messages': Message.objects.filter(chat=chat)}
            messages = Message.objects.filter(chat=chat, was_call=False)
            for msg in messages:
                msg.was_call = True
                msg.save()
            new_messages = NewMessage.objects.filter(to_user=request.user)
            for msg in new_messages:
                msg.delete()
            return render(request, 'userprofile/messages.html', context)

    def post(self, request):
        locale.setlocale(locale.LC_ALL, "")
        """Сохранить новое сообщение"""
        if request.is_ajax():
            ajax = json.loads(request.body.decode('utf-8'))
            chat = Chat.objects.get(pk=ajax.get('chat'))
            message = Message(
                chat=chat,
                author=request.user,
                text=ajax.get('text')
            )
            message.save()
            users_in_chat = chat.user.all()
            for user in users_in_chat:
                if user != request.user:
                    new_msg = NewMessage(message=message, to_user=user)
                    new_msg.save()

            msg_datetime = message.datetime + timedelta(hours=3)
            msg_datetime = msg_datetime.strftime('%d %B %Y г. %H:%M')

            result = {
                'datetime': msg_datetime,
                'text': message.text,
                'chat': ajax.get('chat')
            }
            return JsonResponse(result)


class CreateChat(View):
    def get(self, request, pk):
        addressee = IntergalacticUser.objects.get(pk=pk)
        chat = Chat()
        chat.save()
        request.user.chat_set.add(chat)
        addressee.chat_set.add(chat)
        return HttpResponseRedirect(reverse('profile:correspondence'))


def task(request, chat):
    locale.setlocale(locale.LC_ALL, "")
    for _ in range(30):
        messages = NewMessage.objects.filter(to_user=request.user)
        if messages:
            result = {'msgs': []}
            for msg in messages:
                msg_datetime = msg.message.datetime + timedelta(hours=3)
                msg_datetime = msg_datetime.strftime('%d %B %Y г. %H:%M')

                result['msgs'].append({
                    'datetime': msg_datetime,
                    'text': msg.message.text,
                    'chat': chat,
                })
            messages.delete()
            return JsonResponse(result)
        sleep(1)
    return JsonResponse({'msgs': 'retry'})
