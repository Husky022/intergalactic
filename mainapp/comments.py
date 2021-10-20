from django.template.loader import render_to_string
from mainapp.models import Article, Comment, SubComment


def add_item(item, comment_list):
    item_comment = Comment.objects.filter(article=item).count()
    item.item_comment = item_comment
    comment_list.append(item)


def parse_comment_all(comment_list):
    for item in Article.objects.all():
        add_item(item, comment_list)


def parse_comment_filter(comment_list, self):
    for item in Article.objects.filter(hub__id=self.kwargs['pk']):
        add_item(item, comment_list)


def if_comment_article(self, comment_list):
    if self.kwargs.get("pk", None):
        parse_comment_filter(comment_list, self)
    else:
        parse_comment_all(comment_list)


def comment_main():
    comment_list = []
    parse_comment_all(comment_list)
    return comment_list


def comment_article(self):
    comment_list = []
    if_comment_article(self, comment_list)
    return comment_list


def comment_article_page_get(self):
    self.object = self.get_object()
    context = self.get_context_data(object=self.get_object())
    comments = Comment.objects.filter(article_id=self.kwargs["pk"])
    context['comments'] = comments
    subcomments_dict = {}
    for comment in comments:
        subcomments = SubComment.objects.filter(comment_id=comment.id)
        subcomments_dict[comment] = list(subcomments)
    context['subcomments'] = subcomments_dict
    return context


def comment_article_page_post(self):
    print('POST')
    print(self.request.POST.dict())
    if 'text_comment' in self.request.POST.dict():
        comment = Comment.objects.create(article_id=int(self.kwargs["pk"]), author_id=self.request.user.id,
                                         text=self.request.POST.dict()['text_comment'])
        comment.save()
    elif 'text_subcomment' in self.request.POST.dict():
        subcomment = SubComment.objects.create(comment_id=self.request.POST.dict()['comment_id'], author_id=self.request.user.id,
                                         text=self.request.POST.dict()['text_subcomment'])
        subcomment.save()



def comment_article_page_ajax(self):
    print('GET')
    print(self.request.GET.dict())
    if 'text_comment' in self.request.GET.dict():
        comment = Comment.objects.create(article_id=int(self.kwargs["pk"]), author_id=self.request.user.id,
                                         text=self.request.GET.dict()['text_comment'])
        comment.save()
    elif 'text_subcomment' in self.request.GET.dict():
        print(self.request.GET.dict()['comment_id'])
        print(self.request.GET.dict()['text_subcomment'])

        subcomment = SubComment.objects.create(comment_id=self.request.GET.dict()['comment_id'], author_id=self.request.user.id,
                                         text=self.request.GET.dict()['text_subcomment'])
        print(subcomment.comment_id)
        print(subcomment.author_id)
        print(subcomment.text)
        subcomment.save()


class CommentAction:
    types = {
        'main': comment_main,
        'article': comment_article,
        'article_page_get': comment_article_page_get,
        'article_page_post': comment_article_page_post,
        'article_page_ajax': comment_article_page_ajax,
    }

    @classmethod
    def create(cls, type_, *args):
        return cls.types[type_](*args)
