from django.urls import path
from .views import Main, Articles, Hub_category, article_page, ArticleCreationView, ArticleChangeActiveView, \
    ArticleEditView

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('articles/', Articles.as_view(), name='articles'),
    path('article_page/<int:article_pk>/', article_page, name='article_page'),
    path('hub/<int:hub_id>/', Hub_category.as_view(), name='hub_category'),
    path('create_article/', ArticleCreationView.as_view(), name='create_article'),
    path('change_active/<int:article_pk>/', ArticleChangeActiveView.as_view(), name='change_active'),
    path('edit_active/<int:article_pk>/', ArticleEditView.as_view(), name='edit_article'),
]
