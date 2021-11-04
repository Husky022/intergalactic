from django.urls import path
from moderation.views import Moderator, ModerationArticleView, RegisterNewMessage, ApproveArticle, RejectArticle, ModerateComplaints, ModerationArticleComplaintView, RegisterNewComplaintMessage

app_name = 'moderation'

urlpatterns = [
    path('', Moderator.as_view(), name='main'),
    path('article/<int:pk>/', ModerationArticleView.as_view(), name='article'),
    path('new_message/', RegisterNewMessage.as_view(), name='new_message'),
    path('new_complaint_message/', RegisterNewComplaintMessage.as_view(),
         name='new_complaint_message'),
    path('approve_article/<int:pk>/',
         ApproveArticle.as_view(), name='approve_article'),
    path('reject_article/<int:pk>/',
         RejectArticle.as_view(), name='reject_article'),
    path('complaints', ModerateComplaints.as_view(), name='complaints'),
    path('contested_article/<int:pk>/',
         ModerationArticleComplaintView.as_view(), name='complainted'),
]
