from .models import Category


def category(request):
    links = Category.objects.all()
    return dict(links=links)
