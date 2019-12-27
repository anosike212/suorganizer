from django.shortcuts import render, get_object_or_404,\
    render_to_response, redirect
from django.http import HttpResponse, Http404
from .models import Tag, Startup, NewsLink
from django.template import loader, RequestContext
from .forms import TagForm, StartupForm, NewsLinkForm
from django.views.generic import View
from .utils import (
    ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin,
    DetailView)
from django.urls import reverse_lazy, reverse
from django.core.paginator import (
    EmptyPage, PageNotAnInteger, Paginator)
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from user.decorators import require_authenticated_permission


class Test(View):
    def get(self, request):
        return render(
            request,
            "organiser/sample.json",
            {})

def startup_detail(request, slug):
    startup = get_object_or_404(Startup, slug__iexact = slug)
    print(request.user.id)
    return render(
        request, 
        "organiser/startup_detail.html",
        {"startup": startup}
    )

class StartupDetail(DetailView):
    model = Startup

class StartupList(View):
    page_kwarg = "page"
    template_name = "organiser/startup_list.html"
    paginate_by = 5

    def get(self, request):
        startups = Startup.objects.all()
        paginator = Paginator(startups, self.paginate_by)
        page_number = request.GET.get(self.page_kwarg)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        if page.has_previous():
            previous_url = "?{pkw}={n}".format(
                pkw = self.page_kwarg, 
                n = page.previous_page_number())
        else:
            previous_url = None
        if page.has_next():
            next_url = "?{pkw}={n}".format(
                pkw = self.page_kwarg,
                n = page.next_page_number())
        else:
            next_url = None
        context = {
            "next_page_url": next_url,
            "previous_page_url": previous_url,
            "startup_list": page,
            "paginator": paginator,
        }
        return render(
            request,
            self.template_name,
            context
        )

@require_authenticated_permission('organiser.add_startup')
class StartupCreate(ObjectCreateMixin, View):
    form_class = StartupForm
    template_name = "organiser/startup_form.html"

@require_authenticated_permission('organiser.change_startup')
class StartupUpdate(ObjectUpdateMixin, View):
    form_class = StartupForm
    model = Startup
    template_name = "organiser/startup_form_update.html"

@require_authenticated_permission('organiser.delete_startup')
class StartupDelete(ObjectDeleteMixin, View):
    model = Startup
    success_url = reverse_lazy("organiser_startup_list")
    template_name = "organiser/startup_confirm_delete.html"

def tag_list(request):
    redirect_url = reverse(
        "organiser_tag_page",
        kwargs = {
            "page_number": 1
        }
    )
    return redirect(redirect_url)

def tag_page_list(request, page_number):
    paginate_by = 5
    tags = Tag.objects.all()
    paginator = Paginator(tags, paginate_by)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    if page.has_previous():
        previous_url = reverse(
            "organiser_tag_page",
            kwargs = {
                "page_number": page.previous_page_number()
            })
    else:
        previous_url = None
    if page.has_next():
        next_url = reverse(
            "organiser_tag_page",
            kwargs = {
                "page_number": page.next_page_number()
            })
    else:
        next_url = None
    context = {
        "is_paginated": page.has_other_pages(),
        "next_page_url": next_url,
        "previous_page_url": previous_url,
        "paginator": paginator,
        "tag_list": page,
    }
    return render(
        request,
        "organiser/tag_list.html",
        context
    )

class TagDetail(DetailView):
    context_object_name = "tag"
    model = Tag
    template_name = "organiser/tag_detail.html"

@login_required
def tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            new_form = form.save()
            return redirect(new_form)
    else:
        form = TagForm()
    return render(
        request,
        'organiser/tag_form.html',
        {'form': form})

class TagUpdate(ObjectUpdateMixin, View):
    form_class = TagForm
    model = Tag
    template_name = "organiser/tag_form_update.html"

class TagDelete(ObjectDeleteMixin, View):
    model = Tag
    success_url = reverse_lazy("organiser_tag_list")
    template_name = "organiser/tag_confirm_delete.html"
        
class NewsLinkCreate(ObjectCreateMixin, View):
    form_class = NewsLinkForm
    template_name = "organiser/newslink_form.html"

class NewsLinkUpdate(View):
    form_class = NewsLinkForm
    template_name = "organiser/newslink_form_update.html"

    def get(self, request, pk):
        newslink = get_object_or_404(
            NewsLink,
            pk = pk)
        return render(
            request,
            self.template_name,
            {
                "form": self.form_class(instance = newslink),
                "newslink": newslink
            }
        )

    def post(self, request, pk):
        newslink = get_object_or_404(
            NewsLink,
            pk = pk)
        bound_form = TagForm(request.POST, instance = newslink)
        if bound_form.is_valid():
            new_newslink = bound_form.save()
            return redirect(new_newslink)
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": bound_form,
                    "newslink": newslink
                }
            )

class NewsLinkDelete(View):

    def get(self, request, pk):
        newslink = get_object_or_404(
            NewsLink,
            pk = pk)
        return render(
            request,
            "organiser/newslink_confirm_delete.html",
            {'newslink': newslink}
        )

    def post(self, request, pk):
        newslink = get_object_or_404(
            NewsLink, 
            pk = pk)
        startup = newslink.startup
        newslink.delete()

#R4v3n