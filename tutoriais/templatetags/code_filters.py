from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='preserve_code')
def preserve_code(value):
    """
    Filter to preserve code formatting exactly as entered
    """
    if value:
        # Just remove HTML tags and decode entities, preserve everything else
        clean_code = re.sub(r'<[^>]*>', '', str(value))
        clean_code = clean_code.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        clean_code = clean_code.replace('&nbsp;', ' ')
        # Remove excessive whitespace between words but preserve line structure
        lines = clean_code.split('\n')
        cleaned_lines = []
        for line in lines:
            # Only clean up excessive spaces within lines, preserve indentation
            cleaned_line = re.sub(r' +', ' ', line.rstrip())
            cleaned_lines.append(cleaned_line)
        clean_code = '\n'.join(cleaned_lines).strip()
        return mark_safe(clean_code)
    return ''