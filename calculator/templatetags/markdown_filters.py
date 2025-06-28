import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def markdown_to_html(text):
    # Convert markdown to HTML
    html = markdown.markdown(text)
    return mark_safe(html)