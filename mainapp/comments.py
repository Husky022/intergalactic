from mainapp.models import Article, Comment


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
    context['comments'] = Comment.objects.filter(article_id=self.kwargs["pk"])
    return context


def comment_article_page_post(self):
    comment = Comment.objects.create(article_id=int(self.kwargs["pk"]), author_id=self.request.user.id,
                                     text=self.request.POST.dict()['text_comment'])
    comment.save()


class CommentAction:
    types = {
        'main': comment_main,
        'article': comment_article,
        'article_page_get': comment_article_page_get,
        'article_page_post': comment_article_page_post
    }

    @classmethod
    def create(cls, type_, *args):
        return cls.types[type_](*args)
