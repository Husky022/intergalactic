from django.urls import path

import userprofile.views as profile


app_name = 'profile'

urlpatterns = [
    path('', profile.UserProfileView.as_view(), name='main'),
    path('create_article/', profile.ArticleCreationView.as_view(), name='create_article'),
    path('change_active/<int:article_pk>/', profile.ArticleChangeActiveView.as_view(), name='change_active'),
    path('edit_article/<int:pk>/', profile.ArticleEditView.as_view(), name='edit_article'),
    path('send_to_moderation/<int:pk>/', profile.SendToModeration.as_view(), name='send_to_moderation'),
    path('draft_article/<int:pk>/', profile.DraftArticle.as_view(), name='draft_article'),
    path('user/<int:pk>/', profile.OtherUserProfile.as_view(), name='user'),
]
