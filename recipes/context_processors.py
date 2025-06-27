from .models import Category


def categories_processor(request):
    """
    Context processor that makes all categories available across all templates.
    """
    return {
        'all_categories': Category.objects.all().order_by('name')
    }