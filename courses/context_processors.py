from .models import Category
from django.conf import settings

def get_categories(request):
    return {
        'all_categories': Category.objects.all(),
        'email': settings.EMAIL_HOST_USER,
    }