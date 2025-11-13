from .models import Category


def categories(request):
    return {
        "nav_categories": Category.objects.filter(is_active=True).order_by("name")
    }


