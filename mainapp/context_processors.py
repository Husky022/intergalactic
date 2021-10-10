from mainapp.models import Hab


def category(request):
    return {"category_menu": Hab.objects.all()}
