from django.urls import path

import authapp.views as authapp


app_name = 'auth'

urlpatterns = [
    path('login/', authapp.LoginView.as_view(), name='login'),
    path('logout/', authapp.LogoutView.as_view(), name='logout'),
    path('register/', authapp.RegisterView.as_view(), name='register'),
    path('edit/', authapp.UserEditView.as_view(), name='edit'),
    path('notifications/', authapp.NotificationView.as_view(), name='notifications'),
    path('blocked/', authapp.BlockedView.as_view(), name='blocked'),
    path('notifications_live/<int:count>/', authapp.notifications_live, name='notifications_live'),
    path('messages_live/<int:count>/', authapp.messages_live, name='messages_live'),
]
