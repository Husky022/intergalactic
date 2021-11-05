# модуль для сохранения кода, не относящегося напрямую к контроллерам
from .models import Complaint, ComplaintMessage
from mainapp.models import Article, Comment, SubComment


def check_complaints():
    moderation_call = '@moderator'
    for comment in Comment.objects.filter(is_active=True, text__startswith=moderation_call):
        complaint = Complaint()
        first_message = ComplaintMessage()
        complaint.article = comment.article
        first_message.article = comment.article
        complaint.complainant = comment.author
        first_message.message_from = comment.author
        complaint_text = comment.text[len(moderation_call):]
        complaint.text = complaint_text
        first_message.text = complaint_text
        complaint.datetime = comment.add_datetime
        first_message.datetime = comment.add_datetime
        # complaint.is_active = True
        complaint.save()
        first_message.complaint = Complaint.objects.last()
        first_message.save()
        comment.delete()
        print('Complaints CHECKED')
