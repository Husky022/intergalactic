def total_rating(article):
    """Подсчет рейтинга"""
    article.rating = (int(article.views) * 2) + (article.count_like * 3) + article.count_dislike + (
            article.count_comment * 4)
    article.save()
    return article
