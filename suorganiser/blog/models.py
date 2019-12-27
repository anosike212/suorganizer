from django.db import models
from organiser.models import Tag, Startup
from django.urls import reverse
from django.conf import settings
from datetime import date


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(
            self.model, using = self._db)

    def published(self):
        return self.get_queryset().published()

    def get_by_natural_key(self, pub_date, slug):
        return self.get(
            pub_date = pub_date,
            slug = slug)


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            pub_date__lte = date.today())


class Post(models.Model):
    title = models.CharField(max_length = 63)
    slug = models.SlugField(
        max_length = 63,
        help_text = "A label for URL config.",
        unique_for_month = "pub_date"
    )
    text = models.TextField()
    pub_date = models.DateField(
        "date published",
        auto_now_add = True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name = "blog_posts",
        on_delete = models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag, blank = True, related_name = "blog_posts"
    )
    startups = models.ManyToManyField(
        Startup, blank = True, related_name = "blog_posts"
    )
    objects = PostManager()

    def natural_key(self):
        return (
            self.pub_date,
            self.slug)
    natural_key.dependencies = [
        'organiser.startup',
        'organiser.tag',
        'user.user'
    ]

    def get_absolute_url(self):
        return reverse(
            'blog_post_detail',
            kwargs = {
                'year': self.pub_date.year,
                'month': self.pub_date.month,
                'slug': self.slug}
        )
    
    def get_update_url(self):
        return reverse(
            'blog_post_update',
            kwargs = {
                'year': self.pub_date.year,
                'month': self.pub_date.month,
                'slug': self.slug}
        )

    def get_delete_url(self):
        return reverse(
            'blog_post_delete',
            kwargs = {
                'year': self.pub_date.year,
                'month': self.pub_date.month,
                'slug': self.slug}
        )

    def get_archive_year_url(self):
        return reverse(
            "blog_post_archive_year",
            kwargs = {
                'year': self.pub_date.year}
        )

    def get_archive_month_url(self):
        return reverse(
            "blog_post_archive_month",
            kwargs = {
                "year": self.pub_date.year,
                "month": self.pub_date.month}
        )

    def formatted_title(self):
        return self.title.title()

    def short_text(self):
        if len(self.text.split()) > 20:
            short = ' '.join(self.text.split()[:20])
            short += ' ...'
        else:
            short = self.text
        return short

    def __str__(self):
        return "{} on {}".format(
            self.title, self.pub_date.strftime('%Y-%m-%d')
        )

    class Meta:
        verbose_name = "blog post"
        ordering = ['-pub_date', 'title']
        get_latest_by = "pub_date"
        permissions = (
            ("view_future_post",
             "Can View Unpublished Post"),
        )