from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def redirect_root(request):
    return redirect("blog_post_list")