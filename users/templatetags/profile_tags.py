from django import template
from django.conf import settings
register = template.Library()

@register.simple_tag
def get_profile_image(profile):
    if profile.profile_image:
        return profile.profile_image.url
    return f'{settings.STATIC_URL}images/nobody.jpg'