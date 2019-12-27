from io import StringIO
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag(
    'blog/includes/partial_post_list.html',
    takes_context = True)
def format_post_list(context, detail_object):
    request = context.get('request')
    is_superuser = request.user.is_superuser
    style = "class = 'meta one-third column'"
    if is_superuser:
        post_list = detail_object.blog_posts.all()
    else:
        style = "style = 'display: none;'"
        post_list = []
    return {
        'blog_post_list': post_list,
        'style': mark_safe(style)
    }
    