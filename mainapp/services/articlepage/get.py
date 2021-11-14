from compat import render_to_string
from django.http import JsonResponse

from mainapp.models import VoiceArticle
from mainapp.services.activity.comment import Comments
from mainapp.services.activity.likes import LikeDislike
from mainapp.services.activity.rating import total_rating
from mainapp.services.activity.views import view_views
from mainapp.services.activity.recommendations import set_recommendations


def get_article_page(self):
    """Сбор контекста и взаимодействие активити"""
    # Добавление и валидация просмотра
    view_views(self)
    # Добавление статистики просмотров у юзера
    set_recommendations(self)

    # Создание контекста
    self.object = self.get_object()
    context = self.get_context_data(object=self.get_object())

    # Набив переменных для простоты чтение кода
    user = self.request.user
    article = context["article"]
    get_dict = self.request.GET.dict()

    # Валидация на добавление или удаление дизлайков или лайков
    change_activity(user, article, get_dict, context)

    # Рендер комментарий и их количества
    context = Comments(user, article).render_context(context)

    # Рендер количества лайков
    context = LikeDislike(user, article, get_dict).render_like_and_dislike(context)

    # Рендер рейтинга
    context["article"] = total_rating(article, user)

    # Рендер аудио
    context['audio'] = VoiceArticle.objects.filter(article=article).first()

    # Возвращаем контекст
    return context


def if_get_ajax(self, context):
    """Рендер json для ajax запроса"""
    result_activity = render_to_string('mainapp/includes/inc__activity.html', context, request=self.request)
    get_dict = self.request.GET.dict()
    if get_dict.get("text_comment", "com_delete"):
        result_comment = render_to_string('mainapp/includes/inc__comment.html', context, request=self.request)
        return JsonResponse({"result_activity": result_activity, "result_comment": result_comment})
    # Отправка аяксу результата
    return JsonResponse({"result_activity": result_activity})


def change_activity(user, article, get_dict, context):
    """Валидация выбора события на странице"""
    if get_dict.get("text_comment"):
        Comments(user, article, get_dict).add_get_or_post()
    elif get_dict.get("com_delete"):
        Comments(user, article, get_dict).delete_get_or_post()
    elif get_dict.get("status"):
        LikeDislike(user, article, get_dict).status_like()
