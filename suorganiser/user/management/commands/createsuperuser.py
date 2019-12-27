from django.utils.text import slugify
from user.models import Profile
from .createuser import Command as BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    def create_user(self, name, username, password):
        new_user = self.User.objects.create_superuser(username, password)
        try:
            Profile.objects.create(
                user = new_user,
                name = name,
                slug = slugify(name))
        except Exception as e:
            raise CommandError(
                "Could not create profile:\n{}".format(
                    '; '.join(e.messages)))
        print("SuperUser created successfully")