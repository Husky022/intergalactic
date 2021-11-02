from django.conf import settings
from django.core.mail import send_mail
from authapp.models import NotificationModel, IntergalacticUser
from mainapp.models import Comment, Article, SubComment, Likes
from moderation.models import ArticleMessage


def notifications_read(self):
    return NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=1)


def notifications_not_read_quantity(self):
    print(NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=0).count())
    return NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=0).count()


class Notification:

    def __init__(self, target_object, target_recipient=None, context=None):
        self.object = target_object
        self.context = context
        if target_recipient:
            self.recipient = target_recipient
        else:
            self.recipient = self.get_recipient()
        self.sender_id = self.get_sender_id()
        self.action = self.get_action()
        self.text = self.get_text()
        self.target = self.get_target()
        self.article_id = self.get_article_id()
        self.comment_id = self.get_comment_id()
        self.subcomment_id = self.get_subcomment_id()
        self.like_id = self.get_like_id()



    def get_sender_id(self):
        for instance in (Comment, SubComment, Article):
            if isinstance(self.object, instance):
                return self.object.author_id
        if  isinstance(self.object, Likes):
            return self.object.user_id
        if  isinstance(self.object, Article):
            if self.context == 'moderation' or self.context == 'moderate_after_edit':
                return self.object.author_id
            else:
                return None
        if  isinstance(self.object, ArticleMessage):
            return self.object.message_from.id
        else:
            return None

    def get_action(self):
        if isinstance(self.object, Comment):
            action = 'оставил комментарий к статье '
            self.theme = 'Комментарий'
            return action
        if isinstance(self.object, SubComment):
            action = 'ответил на комментарий '
            self.theme = 'Ответ на комментарий'
            return action
        if  isinstance(self.object, Likes):
            if self.object.status == "LK":
                action = 'поставил лайк статье '
                self.theme = 'Уведомление о лайке'
                return action
            elif self.object.status == "DZ":
                action = 'поставил дизлайк статье '
                self.theme = 'Уведомление о дизлайке'
                return action
        if  isinstance(self.object, Article):
            if self.context == 'published':
                action = 'после рассмотрения опубликована Ваша статья '
                self.theme = 'Публикация статьи'
                return action
            elif self.context == 'rejected':
                action = 'для публикации требуется иправить(доработать) статью '
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
        if  isinstance(self.object, ArticleMessage):
            action = 'оставил сообщение при модерации статьи '
            self.theme = 'Модерация'
            return action
        else:
            return None

    def get_text(self):
        for instance in (Comment, SubComment, ArticleMessage):
            if isinstance(self.object, instance):
                return self.object.text
        else:
            return None

    def get_target(self):
        if isinstance(self.object, Comment):
            article = Article.objects.filter(id=self.object.article_id).first()
            target = article.name
            return target
        if isinstance(self.object, SubComment):
            comment = Comment.objects.filter(id=self.object.comment_id).first()
            target = comment.text
            return target
        if  isinstance(self.object, Likes):
            article = Article.objects.filter(id=self.object.article_id).first()
            target = article.name
            return target
        if  isinstance(self.object, Article):
            return self.object.name
        if  isinstance(self.object, ArticleMessage):
            return self.object.article.name
        else:
            return None

    def get_article_id(self):
        if isinstance(self.object, Comment):
            return self.object.article_id
        if isinstance(self.object, SubComment):
            return self.object.article_id
        if isinstance(self.object, Likes):
            return self.object.article_id
        if  isinstance(self.object, Article):
            return self.object.id
        if  isinstance(self.object, ArticleMessage):
            return self.object.article.id
        else:
            return None

    def get_recipient(self):
        if  isinstance(self.object, Comment):
            article = Article.objects.filter(id=self.object.article_id).first()
            recipient_id = article.author_id
            recipient = IntergalacticUser.objects.filter(id=recipient_id).first()
            return recipient
        if  isinstance(self.object, SubComment):
            comment = Comment.objects.filter(id=self.object.comment_id).first()
            recipient_id = comment.author_id
            recipient = IntergalacticUser.objects.filter(id=recipient_id).first()
            return recipient
        if  isinstance(self.object, Likes):
            article = Article.objects.filter(id=self.object.article_id).first()
            recipient_id = article.author_id
            recipient = IntergalacticUser.objects.filter(id=recipient_id).first()
            return recipient
        if  isinstance(self.object, Article):
            if self.context == 'moderation':
                recipient = IntergalacticUser.objects.filter(is_superuser=True).first()
                return recipient
            if self.context == 'moderate_after_edit':
                recipient = IntergalacticUser.objects.filter(is_superuser=True).first()
                return recipient
            if self.context == 'archive':
                recipient_id = self.object.author_id
                recipient = IntergalacticUser.objects.filter(id=recipient_id).first()
                return recipient
            else:
                recepient_id = self.object.author_id
                recipient = IntergalacticUser.objects.filter(id=recepient_id).first()
                return recipient
        if  isinstance(self.object, ArticleMessage):
            recipient_id = self.object.article.author_id
            recipient = IntergalacticUser.objects.filter(id=recipient_id).first()
            return recipient

    def get_comment_id(self):
        if isinstance(self.object, Comment):
            return self.object.id
        else:
            return None

    def get_subcomment_id(self):
        if isinstance(self.object, SubComment):
            return self.object.id
        else:
            return None

    def get_like_id(self):
        if isinstance(self.object, Likes):
            return self.object.id
        else:
            return None

    def get_theme(self):
        return None



    def send(self):
        notification = NotificationModel.objects.create(recipient=self.recipient,
                                                        sender_id=self.sender_id,
                                                        action=self.action,
                                                        text=self.text,
                                                        target=self.target,
                                                        article_id=self.article_id,
                                                        comment_id=self.comment_id,
                                                        subcomment_id=self.subcomment_id,
                                                        like_id=self.like_id)
        notification.save()
        if self.recipient.send_to_email:
            if self.sender_id:
                user = IntergalacticUser.objects.filter(id=self.sender_id).first()
                username = user.username
            else:
                username = ''
            article = Article.objects.filter(id=self.article_id).first()
            if self.text:
                text = self.text
            else:
                text = ''
            mail_text = f'{username} {self.action} {article.name} {text}'
            send_mail(self.theme, mail_text, settings.EMAIL_HOST_USER, ['test-intergalactic@mail.ru'])


