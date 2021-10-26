from authapp.models import Notification


class NewNotification:

    action = {
        'like_article': 'лайкнул статью: ',
        'dislike_article': 'лайкнул комментарий: ',
        'like_comment': 'дизлайкнул статью: ',
        'dislike_comment': 'дизлайкнул комментарий: ',
        'comment': 'оставил комментарий к статье: ',
        'subcomment': 'ответил на комментарий: ',
        'message': 'прислал сообщение: '
    }

    @classmethod
    def create(cls, type, recipient_user, user, message, target):
        notification = Notification.objects.create(recipient=recipient_user,
                                                   sender_id=user.id,
                                                   action=cls.action[type],
                                                   text=message,
                                                   target=target)
        notification.save()





    # @classmethod
    # def delete(cls, type_, *args):
    #     return cls.types[type_](*args)