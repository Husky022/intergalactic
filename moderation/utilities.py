# модуль для сохранения кода, не относящегося напрямую к контроллерам
from .models import Complaint
from mainapp.models import Comment, SubComment


def check_complaints():
    moderation_call = '@moderator'
    for comment in Comment.objects.filter(is_active=True, text__startswith=moderation_call):
        complaint = Complaint()
        complaint.article = comment.article
        complaint.complainant = comment.author
        complaint_text = comment.text[len(moderation_call):]
        complaint.text = complaint_text
        complaint.datetime = comment.add_datetime
        # complaint.is_active = True
        complaint.save()
        comment.delete()
        print('Complaints CHECKED')
