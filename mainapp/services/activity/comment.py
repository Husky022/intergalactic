from authapp.models import NotificationModel
from authapp.services.notifications import Notification
from mainapp.models import Comment


class Comments:
    """Комментарии"""

    def __init__(self, user, article, get_post=None):
        """Инициализация комментариев и их комментариев"""

        self.user = user
        self.article = article
        self.get_post = get_post

    def add_get_or_post(self):
        """Сохранение комментарий и их комментарий"""
        comment = Comment.objects.create(article=self.article, author=self.user,
                                         text=self.get_post['text_comment'],
                                         parent_id=self.get_post.get("comment_id", None))
        comment.save()
        notification = Notification(comment)
        notification.send()

    def delete_get_or_post(self):
        """Сохранение удаление комментариев и их комментариев"""
        comment = Comment.objects.get(id=self.get_post["com_delete"])
        notification = NotificationModel.objects.filter(comment_id=comment.id)
        notification.delete()
        comment.is_active = False
        comment.save()

    def article_count_comment(self, context):
        count_comment = len(context["comments"])
        if self.article.count_comment != count_comment:
            self.article.count_comment = count_comment
            self.article.save()
        return self.article

    def render_context(self, context):
        """Рендер контекста"""
        context["comments"] = Comment.objects.filter(
            article=self.article, is_active=True).exclude(text__startswith='@moderator')
        context["article"] = self.article_count_comment(context)
        return context
