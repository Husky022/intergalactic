from mainapp.models import Article, ArticleStatus, Comment, SubComment


def parse_all():
    return Article.objects.filter(is_active=True)


def parse_filter(self):
    return Article.objects.filter(
        hub__id=self.kwargs['pk'],
        is_active=True,
        article_status_new=ArticleStatus.objects.get(name='Опубликована')
    )


def add_item(item, comment_list):
    item_comment = Comment.objects.filter(article=item).count()
    item.item_comment = item_comment
    comment_list.append(item)


def parse_comment(type_, comment_list, *args):
    for item in CommentParse.create(type_, *args):
        add_item(item, comment_list)


def if_comment_article(comment_list, self):
    if self.kwargs.get("pk", None):
        parse_comment("filter", comment_list, self)
    else:
        parse_comment("all", comment_list)


def comment(self):
    comment_list = []
    if_comment_article(comment_list, self)
    return comment_list


class CommentParse:
    types = {
        'all': parse_all,
        'filter': parse_filter,
    }

    @classmethod
    def create(cls, type_, *args):
        return cls.types[type_](*args)
