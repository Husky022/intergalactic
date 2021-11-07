"""Модуль лайки и дизлайки"""
from authapp.models import NotificationModel
from authapp.services.notifications import Notification
from mainapp.models import Likes


class LikeDislike(object):
    """Лайки и дизлайки"""

    def __init__(self, user, article):
        """Инициализация лайка для usera, прием реквеста и кваргс"""
        self.user = user
        self.article = article
        self.like = self.change_like()

    def change_like(self):
        """Выбор состояние лайка по отношению зарегистрирован или нет и нахождения usera в этот момент"""
        if self.user.is_anonymous:
            self.like = Likes
        else:
            if Likes.objects.filter(article=self.article, user=self.user):
                self.like = Likes.objects.get(article=self.article, user=self.user)
            else:
                self.like = Likes.objects.create(article=self.article, user=self.user)
        return self.like

    def render_like_and_dislike(self):
        """Рендер количества лайков и дизлайков"""
        self.article.count_like = self.define_count_like("LK")
        self.article.count_dislike = self.define_count_like("DZ")
        self.article.save()
        return self.article

    def define_count_like(self, status):
        """Выбор статуса лайков и дизлайков для рендера"""
        return len(Likes.objects.filter(article=self.article, status=status))

    def status_like(self, status):
        """Сохранение статуса лайка и дизлайка"""
        status = status
        if self.like.status == status:
            notification = NotificationModel.objects.filter(like_id=self.like.id)
            notification.delete()
            self.like.status = "UND"
        else:
            notification = NotificationModel.objects.filter(like_id=self.like.id)
            notification.delete()
            self.like.status = status
            notification = Notification(self.like)
            notification.send()
        self.like.save()
        return self.like.status
