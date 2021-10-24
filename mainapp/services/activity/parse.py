from mainapp.models import Article, Comment, Likes, SubComment


def parse_all():
    return Article.objects.filter(is_active=True)


def parse_filter(self):
    return Article.objects.filter(hub__id=self.kwargs['pk'], is_active=True)


def add_item(item, comment_list):
    item.item_comment = Comment.objects.filter(article=item).count() + SubComment.objects.filter(article=item).count()
    item.item_like = Likes.objects.filter(article=item, status=True).count()
    comment_list.append(item)


def for_parse(type_, comment_list, *args):
    for item in Parse.create(type_, *args):
        add_item(item, comment_list)


def if_article(comment_list, self):
    if self.kwargs.get("pk", None):
        for_parse("filter", comment_list, self)
    else:
        for_parse("all", comment_list)


def queryset_activity(self):
    comment_list = []
    if_article(comment_list, self)
    return comment_list


class Parse:
    types = {
        'all': parse_all,
        'filter': parse_filter
    }

    @classmethod
    def create(cls, type_, *args):
        return cls.types[type_](*args)
