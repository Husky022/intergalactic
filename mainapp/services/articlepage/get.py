from mainapp.models import VoiceArticle
from mainapp.services.activity.comment import Comments
from mainapp.services.activity.likes import LikeDislike
from mainapp.services.activity.rating import total_rating
from mainapp.services.activity.views import view_views


def get_article_page(self):
    """Сбор контекста и взаимодействие активити"""
    # Добавление и валидация просмотра
    view_views(self)

    # Создание контекста
    self.object = self.get_object()
    context = self.get_context_data(object=self.get_object())

    # Набив переменных для простоты чтение кода
    user = self.request.user
    article = context["article"]
    get_dict = self.request.GET.dict()

    # Валидация на добавление или удаление дизлайков или лайков
    if get_dict.get("text_comment"):
        Comments(user, article, get_dict).add_get_or_post()
    elif get_dict.get("com_delete"):
        Comments(user, article, get_dict).delete_get_or_post()
    elif get_dict.get("status"):
        context['article'] = LikeDislike(user, article).status_like(get_dict.get("status"))

    # Рендер статуса лайка
    context['likes'] = LikeDislike(user, article).like

    # Рендер комментарий и их количества
    context = Comments(user, article).render_context(context)

    # Рендер рейтинга
    context["article"] = total_rating(article, user)

    # Рендер аудио
    context['audio'] = VoiceArticle.objects.filter(article=article).first()

    #Возвращаем контекст
    return context
