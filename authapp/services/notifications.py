from authapp.models import NotificationModel



def notifications_read(self):
    return NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=1)


def notifications_not_read_quantity(self):
    print(NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=0).count())
    return NotificationModel.objects.filter(recipient_id=self.request.user.id, is_read=0).count()


class Notification:


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
    def create(cls, type, recipient_user, user, message, target, article_id, comment_id, subcomment_id):
        notification = NotificationModel.objects.create(recipient=recipient_user,
                                                        sender_id=user.id,
                                                        action=cls.action[type],
                                                        text=message,
                                                        target=target,
                                                        article_id=article_id,
                                                        comment_id=comment_id,
                                                        subcomment_id=subcomment_id)
        notification.save()


    @classmethod
    def delete(cls, comment_id):
        notification = NotificationModel.objects.filter(comment_id=comment_id)
        notification.delete()
