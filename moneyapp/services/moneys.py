from authapp.models import IntergalacticUser
from mainapp.models import Article
from moneyapp.models import Transaction, UserBalance


def make_donations(self, donation_data):
    donation = donation_data.dict()
    article = Article.objects.filter(id=int(self.kwargs["pk"]), ).first()
    recipient = IntergalacticUser.objects.filter(id=article.author_id).first()

    new_transaction = Transaction.objects.create(to_user=recipient,
                                                 sender=donation['select'],
                                                 message=donation['message'],
                                                 coins=donation['cash'])
    new_transaction.save()

def transaction_action(self, transaction_data):
    data = transaction_data.dict()
    if 'transaction-reject' in data:
        transaction = Transaction.objects.filter(id=data['transaction-reject']).first()
        transaction.status = 'CANCELLED'
        transaction.save()
    if 'transaction-approve' in data:
        transaction = Transaction.objects.filter(id=data['transaction-approve']).first()
        user_balance = UserBalance.objects.filter(user_id=transaction.to_user_id).first()
        user_balance.amount += transaction.coins
        user_balance.save()
        transaction.status = 'DONE'
        transaction.save()

