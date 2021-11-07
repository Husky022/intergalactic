from django.urls import path
from moneyapp.views import UserFinanceView

app_name = 'moneyapp'

urlpatterns = [
    path('finance/', UserFinanceView.as_view(), name='finance'),
]