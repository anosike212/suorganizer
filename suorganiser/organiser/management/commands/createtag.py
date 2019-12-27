from django.core.management.base import (
    BaseCommand, CommandError)
from django.utils.text import slugify

from ...models import Tag


class Command(BaseCommand):
    help = "Create new Tag:"

    def add_arguments(self, parser):
        parser.add_argument(
            'tag_name',
            default = None,
            help = 'New tag name.')

    def handle(self, **options):
        tag_name = options.get('tag_name', None)
        print(options)
        Tag.objects.create(
            name = tag_name,
            slug = slugify(tag_name))