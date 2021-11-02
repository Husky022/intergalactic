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
        if  isinstance(self.object, Comment):
            return self.object.author_id
        if  isinstance(self.object, SubComment):
            return self.object.author_id
        if  isinstance(self.object, Likes):
            return self.object.user_id
        if  isinstance(self.object, Article):
            if self.context == 'moderation':
                return self.object.author_id
            if self.context == 'moderate_after_edit':
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
            return action
        if isinstance(self.object, SubComment):
            action = 'ответил на комментарий '
            return action
        if  isinstance(self.object, Likes):
            if self.object.status == "LK":
                action = 'поставил лайк статье '
                return action
            elif self.object.status == "DZ":
                action = 'поставил дизлайк статье '
                return action
        if  isinstance(self.object, Article):
            if self.context == 'published':
                action = 'после рассмотрения опубликована Ваша статья '
                return action
            elif self.context == 'rejected':
                action = 'для публикации требуется иправить(доработать) статью '
                return action
            elif self.context == 'moderation':
                action = 'отправил на модерацию статью '
                return action
            elif self.context == 'moderate_after_edit':
                action = 'отредактировал и отправил на модерацию статью '
                return action
            elif self.context == 'archive':
                action = 'отправлена в архив статья: '
                return action
        if  isinstance(self.object, ArticleMessage):
            action = 'оставил сообщение при модерации статьи '
            return action
        else:
            return None

    def get_text(self):
        if isinstance(self.object, Comment):
            return self.object.text
        if isinstance(self.object, SubComment):
            return self.object.text
        if  isinstance(self.object, Article):
            return None
        if  isinstance(self.object, ArticleMessage):
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

    def get_type_object(self):
        pass



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


    # @classmethod
    # def create_notification(cls, type, recipient_user, user, message, target, article_id, comment_id, subcomment_id):
    # # def create(cls, target_object):
    #     notification = NotificationModel.objects.create(recipient=recipient_user,
    #                                                     sender_id=user.id,
    #                                                     action=cls.action[type],
    #                                                     text=message,
    #                                                     target=target,
    #                                                     article_id=article_id,
    #                                                     comment_id=comment_id,
    #                                                     subcomment_id=subcomment_id)
    #     notification.save()


    # @classmethod
    # def delete(cls, comment_id):
    #     notification = NotificationModel.objects.filter(comment_id=comment_id)
    #     notification.delete()


# class Notification:
#     """Фабрика для фильтров"""
#     types = {
#         'add_comment': TypeNotifications.parse_all,
#         # 'add_subcomment': RenderArticle.parse_filter,
#         # 'add_like': RenderArticle.parse_filter,
#         # 'add_dislike': RenderArticle.parse_filter,
#     }
#
#     @classmethod
#     def create(cls, type_, *args):
#         return cls.types[type_](*args)