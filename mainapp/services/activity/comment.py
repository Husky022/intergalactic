from mainapp.models import SubComment, Comment


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

    def add_sub_comment(self):
        """Добавление под комментариев"""
        subcomment = SubComment.objects.create(
            comment_id=self.get_post['comment_id'],
            author=self.user,
            text=self.get_post['text_subcomment'],
            article_id=int(self.pk),
        )
        subcomment.save()

    def add_get_or_post(self):
        """Сохранение комментарий и их комментарий"""
        if 'text_comment' in self.get_post:
            self.add_comment()
        elif 'text_subcomment' in self.get_post:
            self.add_sub_comment()
        return

    def delete_comment(self):
        """Удаление комментария"""
        comment = Comment.objects.filter(id=self.get_post["com_delete"]).first()
        sub_comment = SubComment.objects.filter(comment=comment)
        for item in sub_comment:
            item.is_active = False
            item.save()
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

    def set(self, context):
        """Показ комментариев и лайков"""
        self.add_get_or_post()
        context = self.render_context(context)
        return context

    def delete(self, context):
        """Показ комментариев и лайков"""
        self.delete_get_or_post()
        context = self.render_context(context)
        return context
