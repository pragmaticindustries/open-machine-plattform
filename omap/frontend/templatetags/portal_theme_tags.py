from django import template
from django.core.files.storage import default_storage

register = template.Library()


@register.simple_tag
def get_image_location(file):
    return default_storage.url(file)
