from authapp.models import NotificationModel
from authapp.services.notifications import Notification
from mainapp.models import SubComment, Comment


class CommentSubcomment:
    """Комментарии и их комментарии"""

    def __init__(self, user, article, get_post=None):
        """Инициализация комментариев и их комментариев"""

        self.user = user
        self.article = article
        self.get_post = get_post

    def add_comment(self):
        """Добавление комментариев"""
        comment = Comment.objects.create(article=self.article, author=self.user,
                                         text=self.get_post['text_comment'])
        comment.save()
        return comment

    def add_sub_comment(self):
        """Добавление под комментариев"""
        sub_comment = Comment.objects.create(
            author=self.user,
            text=self.get_post['text_subcomment'],
            article=self.article,
            sub_comment=True,
        )
        sub_comment.save()
        print(self.get_post)
        comment = Comment.objects.get(pk=self.get_post['comment_id'])
        comment.parent = sub_comment
        comment.save()
        return comment

    def add_get_or_post(self):
        """Сохранение комментарий и их комментарий"""
        if 'text_comment' in self.get_post:
            comment = self.add_comment()
            # notification = Notification(comment)
            # notification.send()
        elif 'text_subcomment' in self.get_post:
            subcomment = self.add_sub_comment()
            # notification = Notification(subcomment)
            # notification.send()

    def delete_comment(self):
        """Удаление комментария"""
        comment = Comment.objects.get(id=self.get_post["com_delete"])
        sub_comment = SubComment.objects.filter(comment=comment)
        for item in sub_comment:
            item.is_active = False
            item.save()
            notification_sub = NotificationModel.objects.filter(subcomment_id=item.id)
            notification_sub.delete()
        notification = NotificationModel.objects.filter(comment_id=comment.id)
        notification.delete()
        return comment

    def delete_sub_comment(self):
        """Удаление под комментария"""
        comment = SubComment.objects.get(id=self.get_post["sub_com_delete"])
        return comment

    def delete_get_or_post(self):
        """Сохранение удаление комментариев и их комментариев"""
        if 'com_delete' in self.get_post:
            comment = self.delete_comment()
        elif 'sub_com_delete' in self.get_post:
            comment = self.delete_sub_comment()
        comment.is_active = False
        comment.save()
        notification = NotificationModel.objects.filter(subcomment_id=comment.id)
        notification.delete()

    def parse_sub_comment(self):
        """Парсинг комментариев под комментариями"""
        sub_comments_dict = {}
        for comment in Comment.objects.filter(article=self.article, is_active=True):
            sub_comments = SubComment.objects.filter(comment_id=comment.id, is_active=True)
            sub_comments_dict[comment] = list(sub_comments)
        return sub_comments_dict

    def article_count_commnet_and_sub_comment(self, context):
        count_comment = len(context["comments"])
        count_sub_comment = len(SubComment.objects.filter(article=self.article, is_active=True))
        count_all = count_comment + count_sub_comment
        if self.article.count_comment_and_sub_comment != count_all:
            self.article.count_comment_and_sub_comment = count_all
            self.article.save()
        return self.article

    def render_context(self, context):
        """Рендер контекста"""
        context["comments"] = Comment.objects.filter(
            article=self.article, is_active=True).exclude(text__startswith='@moderator')
        context['subcomments'] = self.parse_sub_comment()
        context["article"] = self.article_count_commnet_and_sub_comment(context)
        return context
