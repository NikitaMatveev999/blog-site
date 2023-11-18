from .models import Category


def categories(request):
    categories = Category.objects.all().distinct()
    return {'categories': categories}
