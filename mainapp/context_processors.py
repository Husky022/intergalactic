from mainapp.models import Hub


def category(request):
    return {"category_menu": Hub.objects.all()}
