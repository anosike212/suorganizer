from django.template import Library
from django.utils.safestring import mark_safe


register = Library()

@register.simple_tag
def dembouz():
    return mark_safe("<p>My test tag</p>")