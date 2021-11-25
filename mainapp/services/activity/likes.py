"""Модуль лайки и дизлайки"""
from authapp.models import NotificationModel
from authapp.services.notifications import Notification
from mainapp.models import Likes
from authapp.services.debugger import timing, get_name


class LikeDislike(object):
    """Лайки и дизлайки"""
    @get_name
    def __init__(self, user, article, status: str = '', comment=None):
        """Инициализация лайка для usera, прием реквеста и кваргс"""
        self.user = user
        print(self.user)
        self.article = article
        self.comment = comment
        self.status = status
        self.like = self.change_like()

    @get_name
    def change_like(self):
        """Выбор состояние лайка по отношению зарегистрирован или нет и нахождения usera в этот момент"""
        if self.user.is_anonymous:
            self.like = Likes
        else:
            if Likes.objects.filter(article=self.article, user=self.user, comment=self.comment):
                self.like = Likes.objects.get(article=self.article, user=self.user, comment=self.comment)
                # print(f'юзер1 - {self.like.user.id}')
            else:
                self.like = Likes.objects.create(article=self.article, user=self.user, comment=self.comment)
        #         print(f'до юзер2 - {self.user}')
        #         print(f'юзер2 - {self.like.user.id}')
        # print(f'юзер3 - {self.like.user.id}')
        return self.like

    @get_name
    def define_count_like(self):
        """Сохранение в статье статуса лайков и дизлайков и их количества для рендера"""
        likes = Likes.objects.filter(article=self.article, comment=self.comment)
        if self.comment:
            self.comment.count_like = len(likes.filter(status="LK"))
            self.comment.count_dislike = len(likes.filter(status="DZ"))
            if self.status:
                self.comment.status_like_dislike = self.like.status
            self.comment.save()
        else:
            self.article.count_like = len(likes.filter(status="LK"))
            self.article.count_dislike = len(likes.filter(status="DZ"))
            if self.status:
                self.article.status_like_dislike = self.like.status
            self.article.save()

    @get_name
    def status_like(self):
        """Сохранение статуса лайка и дизлайка"""
        if self.like.status == self.status:
            notification = NotificationModel.objects.filter(like_id=self.like.id)
            notification.delete()
            self.like.status = "UND"
        else:
            notification = NotificationModel.objects.filter(like_id=self.like.id)
            notification.delete()
            self.like.status = self.status
            notification = Notification(self.like)
            notification.send()

        self.like.save()

    @get_name
    def render_like_and_dislike(self, context):
        """Рендер количества лайков и дизлайков"""
        self.define_count_like()
        context["article"] = self.article
        return context
