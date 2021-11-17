from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView

from adminapp.forms import IntergalacticUserAdminEditForm
from authapp.forms import IntergalacticUserRegisterForm
from authapp.models import IntergalacticUser
from moderation.models import BlockedUser
from authapp.models import IntergalacticUser, NotificationModel
from moneyapp.models import UserBalance, Transaction


# @user_passes_test(lambda u: u.is_superuser)
# def admin_main(request):
#     response = redirect('adminapp:users')
#     return response
from moneyapp.services.moneys import transaction_action


def reading_transactions(func):
    def wrapper(self, request, **kwargs):
        res = func(self, request, **kwargs)
        transactions_not_read = Transaction.objects.filter(is_read=0)
        for item in transactions_not_read:
            item.is_read = 1
            item.save()
        return res

    return wrapper


class UserFinanceView(LoginRequiredMixin, ListView):
    model = UserBalance
    template_name = "moneyapp/finance.html"

    def get_context_data(self, **kwargs):
        context = {
            'title': 'финансы',
            'object_list': UserBalance.objects.all().order_by('-update_datetime'),
            'users': IntergalacticUser.objects.all(),
            'notifications_not_read': NotificationModel.objects.filter(is_read=0,
                                                                       recipient=self.request.user.id).count(),
            'transactions_is_read': Transaction.objects.filter(is_read=True, status='CREATED').order_by('-datetime'),
            'transactions_not_read': Transaction.objects.filter(is_read=False, status='CREATED').order_by('-datetime'),
            'transactions_not_read_count': Transaction.objects.filter(is_read=False, status='CREATED').count(),
        }
        return context

    def post(self, *args, **kwargs):
        print(self.request.POST.dict())
        if 'transaction-approve' in self.request.POST.dict() or 'transaction-reject' in self.request.POST.dict():
            transaction_action(self, self.request.POST, self.request.user.id)
        return HttpResponseRedirect(reverse_lazy('moneyapp:finance'))


    @reading_transactions
    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


