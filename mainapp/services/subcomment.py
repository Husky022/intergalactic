from mainapp.models import SubComment, Comment


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
