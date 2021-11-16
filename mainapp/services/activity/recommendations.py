from mainapp.models import Recommendations, Article


def set_recommendations(self):

    if self.request.user.is_authenticated:
        user = self.request.user
        article = self.get_object()
        Recommendations.objects.get_or_create(user=user, article=article)
        recommend_obj = Recommendations.objects.all()
        recommend_by_article = recommend_obj.filter(user=user, article=article).first()
        recommend_by_article.view_count += 1
        recommend_by_article.save()
