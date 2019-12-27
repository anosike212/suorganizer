from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Post
from django.views.generic import View
from .forms import PostForm
from datetime import date

def post_detail(request, year, month, slug):
    post = get_object_or_404(
        Post, 
        pub_date__year = year,
        pub_date__month = month,
        slug__iexact = slug)
    return render(
        request,
        "blog/post_detail.html",
        {"post": post})

class PostList(View):
    def get(self, request):
        post_objs = get_list_or_404(Post, pub_date__lt = date.today())
        if request.user.has_perm('blog.view_future_post'):
            post_list = Post.objects.all()
            dates_list = post_list.dates('pub_date', 'year')
        else:
            post_list = Post.objects.filter(pub_date__lt = date.today())
            dates_list = post_list.dates('pub_date', 'year')
        context = {
            "post_list": post_list,
            "dates_list": dates_list
        }
        return render(
            request,
            "blog/post_list.html",
            context
        )

class PostArchiveYear(View):
    def get(self, request, year):
        post_objs = get_list_or_404(Post, pub_date__year = year)
        post_list = Post.objects.filter(pub_date__year = year)
        date_list = post_list.dates("pub_date", "month")
        unique_year_dates = Post.objects.dates("pub_date", "year")
        unique_years = [dateObj.year for dateObj in unique_year_dates]
        previous_year = None
        next_year = None
        try:
            year = int(year)
            if len(unique_years) > 1:
                if unique_years.index(year) == (len(unique_years) - 1):
                    previous_year = unique_year_dates[unique_years.index(year) - 1]
                elif unique_years.index(year) == 0:
                    next_year = unique_year_dates[unique_years.index(year) + 1]
                elif unique_years.index(year) > 0 and unique_years.index(year) < (len(unique_years) - 1):
                    previous_year = unique_year_dates[unique_years.index(year) - 1]
                    next_year = unique_year_dates[unique_years.index(year) + 1]
            elif len(unique_years) == 1:
                unique_years.index(year)
        except ValueError:
            pass
        context = {
            "post_list": post_list,
            "date_list": date_list,
            "previous_year": previous_year,
            "next_year": next_year,
        }
        return render(
            request,
            "blog/post_archive_year.html",
            context
        )

class PostArchiveMonth(View):
    def get(self, request, year, month):
        post_objs = get_list_or_404(Post, pub_date__year = year, pub_date__month = month)
        year = int(year)
        month = int(month)
        post_objects = Post.objects.all()
        post_objects_dates = post_objects.dates("pub_date", "day")
        post_list = post_objects.filter(pub_date__year = year, pub_date__month = month)
        date_list = post_objects.dates("pub_date", "month")
        try:
            context_month = date_list.filter(pub_date__year = year, pub_date__month = month)[0]
        except IndexError:
            context_month = date(year, month, 1)
        unique_month_for_year = post_objects.dates("pub_date", "month")
        unique_year_month_pair = [str(dateObj.year) + ":" + str(dateObj.month) for dateObj in unique_month_for_year]
        previous_month = None
        next_month = None
        matcher = "{year}:{month}".format(
            year = year,
            month = month)
        try:
            if len(unique_year_month_pair) > 1:
                if unique_year_month_pair.index(matcher) == (len(unique_year_month_pair) - 1):
                    previous_month = unique_month_for_year[unique_year_month_pair.index(matcher) - 1]
                elif (unique_year_month_pair.index(matcher) > 0) and (unique_year_month_pair.index(matcher) < (len(unique_year_month_pair) - 1)):
                    previous_month = unique_month_for_year[unique_year_month_pair.index(matcher) - 1]
                    next_month = unique_month_for_year[unique_year_month_pair.index(matcher) + 1]
                elif (unique_year_month_pair.index(matcher) == 0):
                    next_month = unique_month_for_year[unique_year_month_pair.index(matcher) + 1]
            elif len(unique_year_month_pair) == 0:
                unique_year_month_pair.index(matcher)
        except ValueError:
            pass
        context = {
            "post_list": post_list,
            "month": context_month,
            "next_month": next_month,
            "previous_month": previous_month,

        }
        return render(
            request, 
            "blog/post_archive_month.html",
            context
        )

class PostCreate(View):
    template_name = "blog/post_form.html"
    form_class = PostForm

    def get(self, request):
        return render(
            request,
            self.template_name,
            {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save(request)
            return redirect(new_post)
        else:
            return render(
                request,
                self.template_name,
                {'form': bound_form})

class PostUpdate(View):
    form_class = PostForm
    model = Post
    template_name = "blog/post_update_form.html"

    def get_object(self, year, month, slug):
        return get_object_or_404(
            Post, 
            pub_date__year = year,
            pub_date__month = month,
            slug__iexact = slug)

    def get(self, request, year, month, slug):
        post = self.get_object(year, month, slug)
        context = {
            'form': self.form_class(instance = post),
            'post': post
        }
        return render(
            request,
            self.template_name,
            context)

    def post(self, request, year, month, slug):
        post = self.get_object(year, month, slug)
        bound_form = self.form_class(request.POST, instance = post)
        if bound_form.is_valid:
            new_post = bound_form.save(request)
            return redirect(new_post)
        else:
            context = {
                'form': bound_form,
                'post': post,
            }
            return render(
                request,
                self.template_name,
                context)

class PostDelete(View):

    def get(self, request, year, month, slug):
        post = get_object_or_404(
            Post, 
            pub_date__year = year,
            pub_date__month = month,
            slug__iexact = slug)
        return render(
            request,
            "blog/post_confirm_delete.html",
            {"post": post}
        )

    def post(self, request, year, month, slug):
        post = get_object_or_404(
            Post, 
            pub_date__year = year,
            pub_date__month = month,
            slug__iexact = slug)
        post.delete()
        return redirect("blog_post_list")