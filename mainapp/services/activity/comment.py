from django.template.loader import render_to_string

from authapp.models import IntergalacticUser, NotificationModel
from mainapp.models import SubComment, Comment, Article
from authapp.services.notifications import Notification


def get_or_post(self, get_post):
    article = Article.objects.filter(id=int(self.kwargs["pk"])).first()
    recipient = IntergalacticUser.objects.filter(id=article.author_id).first()
    if 'text_comment' in get_post:
        comment = Comment.objects.create(article_id=int(self.kwargs["pk"]), author_id=self.request.user.id,
                                         text=get_post['text_comment'])
        comment.save()
        Notification.create('comment', recipient, self.request.user, get_post['text_comment'], article.name, int(self.kwargs["pk"]), comment.id, None)
    elif 'text_subcomment' in get_post:
        subcomment = SubComment.objects.create(
            comment_id=get_post['comment_id'],
            author_id=self.request.user.id,
            text=get_post['text_subcomment'],
            article_id=int(self.kwargs["pk"]),
        )
        subcomment.save()
        comment = Comment.objects.filter(id=get_post['comment_id']).first()
        Notification.create('subcomment', recipient, self.request.user, get_post['text_subcomment'], comment.text, int(self.kwargs["pk"]), None, subcomment.id)


def delete(self, get_post, context):
    if 'com_delete' in get_post:
        comment = Comment.objects.filter(id=get_post["com_delete"]).first()
        sub_comment = SubComment.objects.filter(comment=comment)
        for item in sub_comment:
            item.is_active = False
            item.save()
        notification = NotificationModel.objects.filter(comment_id=comment.id)
        notification.delete()
    elif 'sub_com_delete' in get_post:
        comment = SubComment.objects.filter(id=get_post["sub_com_delete"]).first()
    comment.is_active = False
    comment.save()
    notification = NotificationModel.objects.filter(subcomment_id=comment.id)
    notification.delete()
    context['comments'] = Comment.objects.filter(article_id=self.kwargs["pk"], is_active=True)
    context['subcomments'] = parse_sub_comment(self)
    return render_to_string('mainapp/includes/inc__comment.html', context, request=self.request)


def get_comment(self, context):
    get_or_post(self, self.request.GET.dict())
    context['comments'] = Comment.objects.filter(article_id=self.kwargs["pk"], is_active=True)
    context['subcomments'] = parse_sub_comment(self)
    return render_to_string('mainapp/includes/inc__comment.html', context, request=self.request)


def parse_sub_comment(self):
    sub_comments_dict = {}
    for comment in parse_filter(self):
        add_item(sub_comments_dict, comment)
    return sub_comments_dict


def parse_filter(self):
    return Comment.objects.filter(article_id=self.kwargs["pk"])


def add_item(sub_comments_dict, comment):
    sub_comments = SubComment.objects.filter(comment_id=comment.id, is_active=True)
    sub_comments_dict[comment] = list(sub_comments)
