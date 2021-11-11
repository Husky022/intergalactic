from django.core.management.base import BaseCommand

from authapp.models import IntergalacticUser
from moneyapp.models import UserBalance


class Command(BaseCommand):
    help = "Add balance, if any user don't have it"

    def handle(self, *args, **kwargs):
        users = IntergalacticUser.objects.all()
        for user in users:
            if not UserBalance.objects.filter(user_id=user.id).first():
                new_balance = UserBalance.objects.create(user_id=user.id)
                new_balance.save()
