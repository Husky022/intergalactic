from mainapp.models import SubComment, Comment


def get_or_post(self, get_post):
    if 'text_comment' in get_post:
        comment = Comment.objects.create(article_id=int(self.kwargs["pk"]), author_id=self.request.user.id,
                                         text=get_post['text_comment'])
        comment.save()
    elif 'text_subcomment' in get_post:
        subcomment = SubComment.objects.create(
            comment_id=get_post['comment_id'],
            author_id=self.request.user.id,
            text=get_post['text_subcomment'],
            article_id=int(self.kwargs["pk"]),
        )
        subcomment.save()


def parse_sub_comment(self):
    sub_comments_dict = {}
    for comment in parse_filter(self):
        add_item(sub_comments_dict, comment)
    return sub_comments_dict


def parse_filter(self):
    return Comment.objects.filter(article_id=self.kwargs["pk"])


def add_item(sub_comments_dict, comment):
    sub_comments = SubComment.objects.filter(comment_id=comment.id)
    sub_comments_dict[comment] = list(sub_comments)
