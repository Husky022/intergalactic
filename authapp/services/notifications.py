from django.conf import settings
from django.core.mail import send_mail
from authapp.models import NotificationModel, IntergalacticUser
from mainapp.models import Comment, Article, SubComment, Likes
from moderation.models import ArticleMessage, Complaint, ComplaintMessage


def notifications_read(self):
    return NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=1)


def notifications_not_read_quantity(self):
    print(NotificationModel.objects.filter(
        recipient_id=self.request.user.id, is_read=0).count())
    return NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=0).count()


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
        self.subcomment_id = self.get_subcomment_id()
        self.like_id = self.get_like_id()
        self.complaint_id = self.get_complaint_id()

    def get_sender_id(self):
        for instance in (Comment, SubComment):
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
        if isinstance(self.object, SubComment):
            action = 'ответил на комментарий '
            self.theme = 'Ответ на комментарий'
            return action
        if isinstance(self.object, Likes):
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
            action = 'подал жалобу на: '
            self.theme = 'Модерация'
            return action
        if isinstance(self.object, ComplaintMessage):
            action = 'оставил сообщение при обжаловании статьи '
            self.theme = 'Модерация'
            return action
        else:
            return None

    def get_text(self):
        for instance in (Comment, SubComment, ArticleMessage, Complaint, ComplaintMessage):
            if isinstance(self.object, instance):
                return self.object.text
        else:
            return None

    def get_target(self):
        if isinstance(self.object, Comment) or isinstance(self.object, Likes):
            article = Article.objects.filter(id=self.object.article_id).first()
            target = article.name
            return target
        elif isinstance(self.object, SubComment):
            comment = Comment.objects.filter(id=self.object.comment_id).first()
            target = comment.text
            return target
        elif isinstance(self.object, Article):
            return self.object.name
        for instance in (ArticleMessage, Complaint, ComplaintMessage):
            if isinstance(self.object, instance):
                return self.object.article.name
        else:
            return None

    def get_article_id(self):
        for instance in (Comment, SubComment, Likes):
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
        recipients = []
        for instance in (Comment, Likes):
            if isinstance(self.object, instance):
                article = Article.objects.filter(
                    id=self.object.article_id).first()
                recipient_id = article.author_id
                recipient = IntergalacticUser.objects.filter(
                    id=recipient_id).first()
        if isinstance(self.object, SubComment):
            comment = Comment.objects.filter(id=self.object.comment_id).first()
            recipient_id = comment.author_id
            recipient = IntergalacticUser.objects.filter(
                id=recipient_id).first()
        if isinstance(self.object, Article):
            if self.context == 'moderation' or self.context == 'moderate_after_edit':
                recipient = IntergalacticUser.objects.filter(
                    is_superuser=True).first()
            else:
                recepient_id = self.object.author_id
                recipient = IntergalacticUser.objects.filter(
                    id=recepient_id).first()
        if isinstance(self.object, ArticleMessage):
            recipient_id = self.object.article.author_id
            recipient = IntergalacticUser.objects.filter(
                id=recipient_id).first()
        if isinstance(self.object, Complaint):
            # *1: пока выбираем для рассмотрения жалобы админа,
            # позже надо всех модераторов добавить (Дмитрий)
            recipient = IntergalacticUser.objects.get(pk=1)
        if isinstance(self.object, ComplaintMessage):
            if self.object.message_from.id == 1:  # смотри *1 чуть выше
                recipient = self.object.complaint.complainant
            else:
                recipient = IntergalacticUser.objects.get(
                    pk=1)  # смотри *1 чуть выше
        recipients.append(recipient)
        return recipients

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

    def get_complaint_id(self):
        if isinstance(self.object, Complaint):
            return self.object.id
        if isinstance(self.object, ComplaintMessage):
            return self.object.complaint.id
        else:
            return None

    def get_theme(self):
        return None

    def send(self):

        for recipient in self.recipients:
            notification = NotificationModel.objects.create(recipient=recipient,
                                                            sender_id=self.sender_id,
                                                            action=self.action,
                                                            text=self.text,
                                                            target=self.target,
                                                            article_id=self.article_id,
                                                            comment_id=self.comment_id,
                                                            subcomment_id=self.subcomment_id,
                                                            like_id=self.like_id,
                                                            complaint_id=self.complaint_id)
            notification.save()

            if recipient.send_to_email:
                if self.sender_id:
                    user = IntergalacticUser.objects.filter(
                        id=self.sender_id).first()
                    username = user.username
                else:
                    username = ''
                article = Article.objects.filter(id=self.article_id).first()
                if self.text:
                    text = self.text
                else:
                    text = ''
                mail_text = f'{username} {self.action} {article.name} {text}'
                send_mail(self.theme, mail_text, settings.EMAIL_HOST_USER, [
                          'test-intergalactic@mail.ru'])
