from mainapp.models import Article
from mainapp.services.activity.comment import Comments
from mainapp.services.activity.likes import LikeDislike


def post_article_page(self):
    """Взаимодействие активити"""
    # Набив переменных для простоты чтение кода
    user = self.request.user
    article = Article.objects.get(pk=self.kwargs["pk"])
    post_dict = self.request.POST.dict()

    # Валидация на добавление или удаление дизлайков или лайков
    if post_dict.get("text_comment"):
        Comments(user, article, post_dict).add_get_or_post()
    elif post_dict.get("com_delete"):
        Comments(user, article, post_dict).delete_get_or_post()
    elif post_dict.get("status"):
        post_dict['article'] = LikeDislike(user, article, status=post_dict.get('status')).status_like()
