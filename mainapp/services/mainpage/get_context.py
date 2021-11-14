from authapp.models import IntergalacticUser
from mainapp.models import Article, ArticleStatus, Recommendations, Hub
from django.db.models import Sum

def get_context_main_page(self, context):
    status = ArticleStatus.objects.get(name='Опубликована')
    articles = Article.objects.filter(article_status_new=status)
    context['top_news'] = articles.order_by('-add_datetime')[:3]
    context['top_popular'] = articles.order_by('-rating')[:3]
    context['top_views'] = articles.order_by('-views')[:3]
    if not self.request.user.is_anonymous:
        recommend = Recommendations.objects.filter(user=self.request.user)
        context['recommend_articles'] = recommend.order_by('-view_count')[:3]
        recommend_hub_list = recommend.values('article__hub').annotate(views=Sum('view_count')). \
                         order_by('-views')[:3]
        recommend_author_list = recommend.values('article__author').annotate(views=Sum('view_count')). \
                            order_by('-views')[:3]
        hub_pk = []
        authors_pk = []
        for i in recommend_hub_list:
            hub_pk.append(i['article__hub'])
            for i in recommend_author_list:
                authors_pk.append(i['article__author'])
                context['recommend_hubs'] = Hub.objects.filter(pk__in=hub_pk)
                context['recommend_authors'] = IntergalacticUser.objects.filter(pk__in=authors_pk)
    return context