from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from urllib.parse import urlparse

class TagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(
            slug = slug)


class Tag(models.Model):
    name = models.CharField(
        max_length = 31,
        unique = True)
    slug = models.SlugField(
        max_length = 31,
        unique = True,
        help_text = "A label for URL config.")
    objects = TagManager()

    def natural_key(self):
        return (
            self.slug)

    def get_absolute_url(self):
        return reverse(
            'organiser_tag_detail',
            kwargs = {
                'slug': self.slug})

    def get_update_url(self):
        return reverse(
            'organiser_tag_update',
            kwargs = {
                'slug': self.slug})

    def get_delete_url(self):
        return reverse(
            "organiser_tag_delete",
            kwargs = {
                "slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class StartupManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug = slug)


class Startup(models.Model):
    name = models.CharField(
        max_length = 31,
        db_index = True
    )
    slug = models.SlugField(
        max_length = 31,
        unique = True,
        help_text = "A label for URL config."
    )
    description = models.TextField()
    founded_date = models.DateField(verbose_name = "founded date")
    contact = models.EmailField()
    website = models.URLField(max_length = 255)
    tags = models.ManyToManyField(Tag, blank = True)
    objects = StartupManager()

    def natural_key(self):
        return self.slug

    def get_absolute_url(self):
        return reverse(
            'organiser_startup_detail',
            kwargs = {
                'slug': self.slug})

    def get_update_url(self):
        return reverse(
            'organiser_startup_update',
            kwargs = {
                'slug': self.slug})

    def get_delete_url(self):
        return reverse(
            "organiser_startup_delete",
            kwargs = {
                'slug': self.slug})

    def get_feed_atom_url(self):
        return reverse(
            'organiser_startup_atom_feed',
            kwargs = {'startup_slug': self.slug})

    def get_feed_rss_url(self):
        return reverse(
            'organiser_startup_rss_feed',
            kwargs = {'startup_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'


class NewsLinkManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug = slug)


class NewsLink(models.Model):
    title = models.CharField(max_length = 63)
    slug = models.SlugField(max_length = 63)
    pub_date = models.DateField("date published")
    link = models.URLField(max_length = 255)
    startup = models.ForeignKey(Startup, on_delete = models.CASCADE)
    objects = NewsLinkManager()

    def natural_key(self):
        return self.slug
        
    def get_absolute_url(self):
        return self.startup.get_absolute_url() 

    def get_update_url(self):
        return reverse(
            "organiser_newslink_update",
            kwargs = {
                'pk': self.pk})

    def get_delete_url(self):
        return reverse(
            "organiser_newslink_delete",
            kwargs = {
                'pk': self.pk})

    def description(self):
        return (
            "Written on "
            "{0:%A, %B} {0.day}, {0:%Y}; "
            "hosted at {1}".format(
                self.pub_date,
                urlparse(self.link).netloc))

    def __str__(self):
        return "{} : {}".format(
            self.startup, self.title)

    class Meta:
        verbose_name = "news article"
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        unique_together = ('slug', 'startup')