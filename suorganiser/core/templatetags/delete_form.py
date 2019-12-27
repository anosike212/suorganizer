from django.template import Library, TemplateSyntaxError


register = Library()

@register.inclusion_tag(
    'core/includes/delete_form.html')
def delete(*args, **kwargs):
    action = (args[0] if len(args) > 0 else kwargs.get('action'))
    display_attr = (args[1] if len(args) > 1 else kwargs.get('display_attr'))
    cancel_url = (args[2] if len(args) > 2 else kwargs.get('cancel_url'))
    button = (args[3] if len(args) > 3 else kwargs.get('button'))
    method = (args[4] if len(args) > 4 else kwargs.get('method'))

    if (action is None) or (display_attr is None) or (cancel_url is None) :
        raise TemplateSyntaxError(
            'delete template tag '
            'requires at least three attributes:\n'
            'action - which is a URL,\n'
            'display_attr(Title/Name) - which is a string,\n'
            'cancel_url - which is a URL.')
    
    return {
        'action': action,
        'button': button,
        'method': method,
        'display_attr': display_attr,
        'cancel_url': cancel_url,
    }
