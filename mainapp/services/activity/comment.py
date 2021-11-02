from authapp.models import IntergalacticUser, NotificationModel
from authapp.services.notifications import Notification
from mainapp.models import SubComment, Comment, Article


class CommentSubcomment:
    """Комментарии и их комментарии"""

    def __init__(self, request, kwargs, get_post=None):
        """Инициализация комментариев и их комментариев"""
        self.request = request
        self.user = self.request.user
        self.pk = kwargs["pk"]
        if get_post:
            self.get_post = get_post

    def add_comment(self):
        """Добавление комментариев"""
        comment = Comment.objects.create(article_id=int(self.pk), author=self.user,
                                         text=self.get_post['text_comment'])
        comment.save()
        return comment

    def add_sub_comment(self):
        """Добавление под комментариев"""
        subcomment = SubComment.objects.create(
            comment_id=self.get_post['comment_id'],
            author=self.user,
            text=self.get_post['text_subcomment'],
            article_id=int(self.pk),
        )
        subcomment.save()
        return subcomment

    def add_get_or_post(self):
        """Сохранение комментарий и их комментарий"""
        article = Article.objects.filter(id=int(self.pk)).first()
        recipient = IntergalacticUser.objects.filter(id=article.author_id).first()
        if 'text_comment' in self.get_post:
            comment = self.add_comment()
            Notification.create('comment', recipient, self.request.user, self.get_post['text_comment'], article.name,
                                int(self.pk), comment.id, None)
        elif 'text_subcomment' in self.get_post:
            subcomment = self.add_sub_comment()
            comment = Comment.objects.filter(id=self.get_post['comment_id']).first()
            Notification.create('subcomment', recipient, self.request.user, self.get_post['text_subcomment'],
                                comment.text, int(self.pk), None, subcomment.id)

    def delete_comment(self):
        """Удаление комментария"""
        comment = Comment.objects.filter(id=self.get_post["com_delete"]).first()
        sub_comment = SubComment.objects.filter(comment=comment)
        for item in sub_comment:
            item.is_active = False
            item.save()
        notification = NotificationModel.objects.filter(comment_id=comment.id)
        notification.delete()
        return comment

    def delete_sub_comment(self):
        """Удаление под комментария"""
        comment = SubComment.objects.filter(id=self.get_post["sub_com_delete"]).first()
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
        for comment in Comment.objects.filter(article_id=self.pk, is_active=True):
            sub_comments = SubComment.objects.filter(comment_id=comment.id, is_active=True)
            sub_comments_dict[comment] = list(sub_comments)
        return sub_comments_dict

    def render_context(self, context):
        """Рендер контекста"""
        context["comments"] = Comment.objects.filter(article_id=self.pk, is_active=True)
        context['subcomments'] = self.parse_sub_comment()
        context['comments_count'] = len(context['comments']) + len(
            SubComment.objects.filter(article_id=self.pk, is_active=True))
        return context
