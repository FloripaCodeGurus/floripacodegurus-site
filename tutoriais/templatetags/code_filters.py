from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='format_code')
def format_code(value):
    """
    Filter to properly format code blocks by removing HTML tags
    while preserving whitespace and indentation
    """
    if value:
        # Remove HTML tags but preserve line breaks and spaces
        clean_code = re.sub(r'<[^>]*>', '', value)
        # Ensure the output is marked safe to prevent further escaping
        return mark_safe(clean_code)
    return ''