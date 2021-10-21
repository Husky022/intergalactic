from django.template.loader import render_to_string

from mainapp.models import Comment, SubComment
from mainapp.services.subcomment import parse_sub_comment


def fill_context(self):
    self.object = self.get_object()
    context = self.get_context_data(object=self.get_object())
    context['comments'] = Comment.objects.filter(article_id=self.kwargs["pk"])
    context['subcomments'] = parse_sub_comment(self)
    return context


def comment_article_page_get(self, user_like_status, like_count):
    context = fill_context(self)
    context.update(user_like_status=user_like_status, like_count=like_count)
    return context


def get_or_post(self, gp):
    if 'text_comment' in gp:
        comment = Comment.objects.create(article_id=int(self.kwargs["pk"]), author_id=self.request.user.id,
                                         text=gp['text_comment'])
        comment.save()
    elif 'text_subcomment' in gp:
        subcomment = SubComment.objects.create(comment_id=gp['comment_id'],
                                               author_id=self.request.user.id,
                                               text=gp['text_subcomment'])
        subcomment.save()


def comment_article_page_post(self, gp):
    get_or_post(self, gp)


def comment_article_page_ajax(self, user_like_status, like_count, gp):
    get_or_post(self, gp)
    context = CommentAction.create("comment_get", self, user_like_status, like_count)
    result = render_to_string('mainapp/includes/inc__comment.html', context, request=self.request)
    return result


class CommentAction:
    types = {
        'comment_get': comment_article_page_get,
        'comment_post': comment_article_page_post,
        'comment_ajax': comment_article_page_ajax,
    }

    @classmethod
    def create(cls, type_, *args):
        return cls.types[type_](*args)
