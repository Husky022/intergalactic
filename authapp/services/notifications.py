import time

from compat import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from authapp.models import NotificationModel, IntergalacticUser
from intergalactic import settings

from mainapp.models import Comment, Article, Likes
from moderation.models import ArticleMessage, Complaint, ComplaintMessage
import datetime
from background_task import background
from moneyapp.models import Transaction


def notifications_read(self):
    return NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=1)


def notifications_not_read_quantity(self):
    print(NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=0).count())
    return NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=0).count()


@background(schedule=5)
def send_to_email(data):
    theme = data['theme']
    html_message = render_to_string(
        'authapp/email/notifications.html', {'item': data})
    msg = strip_tags(html_message)
    send_mail(theme, msg, settings.EMAIL_HOST_USER, [
              'test-intergalactic@mail.ru'], html_message=html_message)


class Notification:

    def __init__(self, target_object, target_recipient=None, context=None):
        self.object = target_object
        self.context = context
        if target_recipient:
            self.recipient = target_recipient
        else:
            self.recipients = self.get_recipient()
        self.sender_id = self.get_sender_id()
        self.action = self.get_action()
        self.text = self.get_text()
        self.target = self.get_target()
        self.article_id = self.get_article_id()
        self.comment_id = self.get_comment_id()
        self.like_id = self.get_like_id()
        self.complaint_id = self.get_complaint_id()

    def get_sender_id(self):
        for instance in (Comment, Comment):
            if isinstance(self.object, instance):
                return self.object.author_id
        if isinstance(self.object, Likes):
            return self.object.user_id
        if isinstance(self.object, Article):
            if self.context == 'moderation' or self.context == 'moderate_after_edit':
                return self.object.author_id
            else:
                return None
        for instance in (ArticleMessage, ComplaintMessage):
            if isinstance(self.object, instance):
                return self.object.message_from.id
        if isinstance(self.object, Complaint):
            return self.object.complainant.id
        else:
            return None

    def get_action(self):
        if isinstance(self.object, Comment):
            action = 'оставил комментарий к статье '
            self.theme = 'Комментарий'
            return action
        if isinstance(self.object, Likes):
            if self.object.comment_id:
                if self.object.status == "LK":
                    action = 'поставил лайк комментарию '
                    self.theme = 'Уведомление о лайке'
                    return action
                elif self.object.status == "DZ":
                    action = 'поставил дизлайк комментарию '
                    self.theme = 'Уведомление о дизлайке'
                    return action
            else:
                if self.object.status == "LK":
                    action = 'поставил лайк статье '
                    self.theme = 'Уведомление о лайке'
                    return action
                elif self.object.status == "DZ":
                    action = 'поставил дизлайк статье '
                    self.theme = 'Уведомление о дизлайке'
                    return action
        if isinstance(self.object, Article):
            if self.context == 'published':
                action = 'после рассмотрения опубликована Ваша статья '
                self.theme = 'Публикация статьи'
                return action
            elif self.context == 'rejected':
                action = 'для публикации требуется иправить(доработать) статью '
                self.theme = 'Модерация'
                return action
            elif self.context == 'blocked':
                action = 'заблокирована Ваша статья '
                self.theme = 'Модерация'
                return action
            elif self.context == 'moderation':
                action = 'отправил на модерацию статью '
                self.theme = 'Модерация'
                return action
            elif self.context == 'moderate_after_edit':
                action = 'отредактировал и отправил на модерацию статью '
                self.theme = 'Модерация'
                return action
            elif self.context == 'archive':
                action = 'отправлена в архив статья: '
                self.theme = 'Архив'
                return action
        if isinstance(self.object, ArticleMessage):
            action = 'оставил сообщение при модерации статьи '
            self.theme = 'Модерация'
            return action
        if isinstance(self.object, Complaint):
            if self.object.comment:
                action = 'подал жалобу на комментарий: '
                self.theme = 'Жалоба на комментарий'
            else:
                action = 'подал жалобу на статью: '
                self.theme = 'Жалоба на статью'
            return action
        if isinstance(self.object, ComplaintMessage):
            action = 'оставил сообщение при обжаловании статьи '
            self.theme = 'Модерация'
            return action
        if isinstance(self.object, Transaction):
            action = 'Вам отправили вознаграждение! Так держать!'
            self.theme = 'Вознаграждение'
            return action
        else:
            return None

    def get_text(self):
        for instance in (Comment, ArticleMessage, Complaint, ComplaintMessage):
            if isinstance(self.object, instance):
                return self.object.text
        if isinstance(self.object, Transaction):
            return f'{self.object.coins} руб. Сообщение {self.object.message}'

        else:
            return None

    def get_target(self):
        if isinstance(self.object, Comment):
            article = Article.objects.filter(id=self.object.article_id).first()
            target = article.name
            return target
        elif isinstance(self.object, Likes):
            if self.object.comment_id:
                comment = Comment.objects.filter(id=self.object.comment_id).first()
                target = comment.text
            else:
                article = Article.objects.filter(id=self.object.article_id).first()
                target = article.name
            return target
        elif isinstance(self.object, Article):
            return self.object.name
        elif isinstance(self.object, Complaint):
            if self.object.comment:
                return self.object.comment.text
            else:
                print(f'зашёл на артикл {self.object.article.name}')
                return self.object.article.name

        for instance in (ArticleMessage, ComplaintMessage):
            if isinstance(self.object, instance):
                return self.object.article.name
        else:
            return None

    def get_article_id(self):
        for instance in (Comment, Likes):
            if isinstance(self.object, instance):
                return self.object.article_id
        if isinstance(self.object, Article):
            return self.object.id
        for instance in (ArticleMessage, Complaint, ComplaintMessage):
            if isinstance(self.object, instance):
                return self.object.article.id
        else:
            return None

    def get_recipient(self):
        global recipient
        recipients = []
        if isinstance(self.object, Comment):
            article = Article.objects.filter(id=self.object.article_id).first()
            recipient_id = article.author_id
            recipient = IntergalacticUser.objects.filter(id=recipient_id).first()
        if isinstance(self.object, Likes):
            if self.object.comment_id:
                comment = Comment.objects.filter(id=self.object.comment_id).first()
                recipient_id = comment.author_id
                recipient = IntergalacticUser.objects.filter(id=recipient_id).first()
            else:
                article = Article.objects.filter(id=self.object.article_id).first()
                recipient_id = article.author_id
                recipient = IntergalacticUser.objects.filter(id=recipient_id).first()
        elif isinstance(self.object, Article):
            if self.context == 'moderation' or self.context == 'moderate_after_edit':
                recipient = IntergalacticUser.objects.filter(is_superuser=True).first()
            else:
                recepient_id = self.object.author_id
                recipient = IntergalacticUser.objects.filter(
                    id=recepient_id).first()
        elif isinstance(self.object, ArticleMessage):
            if IntergalacticUser.objects.filter(id=self.object.message_from.id).first().is_superuser or IntergalacticUser.objects.filter(id=self.object.message_from.id).first().is_staff:
                recipient_id = self.object.article.author_id
                recipient = IntergalacticUser.objects.filter(id=recipient_id).first()
            else:
                users = IntergalacticUser.objects.all()
                for user in users:
                    if user.is_staff or user.is_superuser:
                        recipients.append(user)
        if isinstance(self.object, Complaint):
            return self.get_stuff_users()
            # *1: пока выбираем для рассмотрения жалобы админа,
            # позже надо всех модераторов добавить (Дмитрий)
            # recipient = IntergalacticUser.objects.get(pk=1)
        if isinstance(self.object, ComplaintMessage):
            if self.object.message_from.id == 1:  # смотри *1 чуть выше
                recipient = self.object.complaint.complainant
            else:
                recipient = IntergalacticUser.objects.get(
                    pk=1)  # смотри *1 чуть выше
        if isinstance(self.object, Transaction):
            recipient = self.object.to_user
        recipients.append(recipient)
        return recipients

    def get_comment_id(self):
        if isinstance(self.object, Comment):
            return self.object.id
        if isinstance(self.object, Likes) and self.object.comment_id:
            return self.object.comment_id
        if isinstance(self.object, Complaint) and self.object.comment:
            return self.object.comment.id
        else:
            return None

    def get_like_id(self):
        if isinstance(self.object, Likes):
            return self.object.id
        else:
            return None

    def get_complaint_id(self):
        if isinstance(self.object, Complaint):
            return self.object.id
        if isinstance(self.object, ComplaintMessage):
            return self.object.complaint.id
        else:
            return None

    def get_theme(self):
        return None

    def get_stuff_users(self):
        result = IntergalacticUser.objects.filter(is_staff=True)
        print(f'РЕЗУЛЬТАТ: {result} тип {type(result)}')
        return result

    def send(self):
        # print('init')
        for recipient in self.recipients:
            # print(recipient.id)
            # print(self.sender_id)
            if recipient.id != self.sender_id:
                # print('init2')
                notification = NotificationModel.objects.create(recipient=recipient,
                                                                sender_id=self.sender_id,
                                                                action=self.action,
                                                                text=self.text,
                                                                target=self.target,
                                                                theme=self.theme,
                                                                article_id=self.article_id,
                                                                comment_id=self.comment_id,
                                                                like_id=self.like_id,
                                                                complaint_id=self.complaint_id)
                # print('init3')
                notification.save()

                if recipient.send_to_email:
                    context = {
                        'recipient': str(notification.recipient),
                        'add_datetime': str(datetime.datetime.now()),
                        'action': notification.action,
                        'text': notification.text,
                        'theme': self.theme,

                    }

                    if notification.sender and notification.target:
                        context.update({
                            'sender': str(notification.sender),
                            'target': notification.target,
                        })

                    send_to_email(context)
