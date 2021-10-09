from mainapp.models import ArticlesCategory

def category(request):
    return {"category_menu": ArticlesCategory.objects.all()}
