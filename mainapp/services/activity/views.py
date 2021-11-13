from mainapp.models import Visits


def view_views(self):
    """Показывает просмотры"""
    user_ip = self.request.get_host()
    if self.request.user.is_authenticated:
        user_name = self.request.user.username
    else:
        user_name = "Anon"
    self.object = self.get_object()
    if Visits.objects.filter(article=self.object, host=user_ip, user=user_name):
        return None
    else:
        self.object.views += 1
        Visits.objects.create(article=self.object, user=user_name, host=user_ip)
        self.object.save()
