from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.urls import reverse
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
            'transactions_is_read': Transaction.objects.filter(is_read=True).order_by('-datetime'),
            'transactions_not_read': Transaction.objects.filter(is_read=False).order_by('-datetime'),
            'transactions_not_read_count': Transaction.objects.filter(is_read=False).count(),
        }
        return context


    @reading_transactions
    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = "пользователи/создание"
#
#     if request.method == "POST":
#         user_form = IntergalacticUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse("adminapp:users"))
#     else:
#         user_form = IntergalacticUserRegisterForm()
#
#     content = {
#         "title": title,
#         "update_form": user_form,
#         "media_url": settings.MEDIA_URL
#     }
#
#     return render(request, "adminapp/user_update.html", content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = "пользователи/редактирование"
#
#     edit_user = get_object_or_404(IntergalacticUser, pk=pk)
#     if request.method == "POST":
#         edit_form = IntergalacticUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse("adminapp:user_update", args=[edit_user.pk]))
#     else:
#         edit_form = IntergalacticUserAdminEditForm(instance=edit_user)
#
#     content = {"title": title, "update_form": edit_form, "media_url": settings.MEDIA_URL}
#
#     return render(request, "adminapp/user_update.html", content)
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = "пользователи/удаление"
#
#     user = get_object_or_404(IntergalacticUser, pk=pk)
#
#     if request.method == "POST":
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse("adminapp:users"))
#
#     content = {"title": title, "user_to_delete": user, "media_url": settings.MEDIA_URL}
#
#     return render(request, "adminapp/user_delete.html", content)
#
# @user_passes_test(lambda u: u.is_superuser)
# def user_blocked(request, pk):
#     title = "пользователи/блокировка"
#
#     user = get_object_or_404(IntergalacticUser, pk=pk)
#
#
#
#     blockedusers = BlockedUser.objects.create(user = user, text = 'text')
#     blockedusers.save()
#     return HttpResponseRedirect(reverse("adminapp:users"))
#
#
#
# def db_profile_by_type(prefix, type, queries):
#     update_queries = list(filter(lambda x: type in x["sql"], queries))
#     print(f"db_profile {type} for {prefix}:")
#     [print(query["sql"]) for query in update_queries]
