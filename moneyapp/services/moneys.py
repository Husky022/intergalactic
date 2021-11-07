from authapp.models import IntergalacticUser
from mainapp.models import Article
from moneyapp.models import Transaction


def make_donations(self, donation_data):
    donation = donation_data.dict()
    article = Article.objects.filter(id=int(self.kwargs["pk"]), ).first()
    recipient = IntergalacticUser.objects.filter(id=article.author_id).first()

    new_transaction = Transaction.objects.create(to_user=recipient,
                                                 sender=donation['select'],
                                                 message=donation['message'],
                                                 coins=donation['cash'])
    new_transaction.save()