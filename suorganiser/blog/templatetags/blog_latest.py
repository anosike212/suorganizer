from django.template import (
    Library, Node, TemplateSyntaxError)
from ..models import Post

register = Library()

@register.tag(name = "get_latest_post")
def do_latest_post(parser, token):
    return LatestPostNode()


class LatestPostNode(Node):
    
    def render(self, context):
        context['latest_post'] = (
            Post.objects.published().latest())
        return str()


@register.tag(name = "get_latest_posts")
def do_latest_posts(parser, token):
    # to get the token arguments: token.contents

    asvar = None
    tag_name, *tokens = token.split_contents()
    if len(tokens) > 2 and tokens[-2] == 'as':
        *tokens, _, asvar = tokens
    if len(tokens) != 1:
        raise TemplateSyntaxError(
            '{name} takes 1 argument:'
            ' the number of posts.'.format(
                name = tag_name))
    try:
        number_of_posts = int(tokens.pop())
    except ValueError:
        raise TemplateSyntaxError(
            "tag '{tag_display}' sole argument "
            "must be an integer".format(
                tag_display = tag_name))
    return LatestPostsNode(number_of_posts, asvar)


class LatestPostsNode(Node):

    def __init__(self, number_of_posts, asvar):
        self.num = number_of_posts
        self.asvar = asvar

    def render(self, context):
        objs = Post.objects.published()[:self.num]
        if self.asvar is None:
            context['latest_posts_list'] = objs
        else:
            context[self.asvar] = objs
        return str()