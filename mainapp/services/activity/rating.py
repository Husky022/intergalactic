from mainapp.models import Article


def total_rating(article, user):
    """Подсчет рейтинга статьи"""
    article.rating = (int(article.views) * 2) + (article.count_like * 3) + article.count_dislike + (
            article.count_comment * 4)
    article.save()
    sum_rating_author(article)
    return article


def sum_rating_author(article):
    author = article.author
    article = Article.objects.filter(author=author)
    sum_article_rating = []
    for item in article:
        sum_article_rating.append(item.rating)
    author.rating_author = sum(sum_article_rating) / 10
    author.save()
