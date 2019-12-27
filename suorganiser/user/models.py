from django.db import models
from datetime import date
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)


class ProfileManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug = slug)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE)
    name = models.CharField(
        max_length = 255)
    slug = models.SlugField(
        max_length = 30,
        unique = True)
    profile_image = models.ImageField(upload_to = "user/profile_images/", blank = True)
    about = models.TextField()
    joined = models.DateTimeField(
        "Date Joined",
        auto_now_add = True)
    objects = ProfileManager()

    def natural_key(self):
        return self.slug

    def get_absolute_url(self):
        return reverse(
            "dj-auth:public_profile",
            kwargs = {
                'slug': self.slug})

    def get_update_url(self):
        return reverse(
            "dj-auth:profile_update")

    def __str__(self):
        return self.user.get_username()
    

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop("is_superuser", False)
        user = self.model(
            email = email,
            is_active = True,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **kwargs)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_user(self, email, password = None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password = None, **extra_fields):
        return self._create_user(email, password, is_staff = True, is_superuser = True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'email address',
        max_length = 254,
        unique = True)
    is_staff = models.BooleanField(
        'staff status',
        default = False,
        help_text = (
            'Designates whether the user can '
            'log into the admin site.'))
    is_active = models.BooleanField(
        'active',
        default = True,
        help_text = (
            'Designates whether this user should '
            'be treated as active. Unselect this '
            'instead of deleting accounts.'))
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def published_posts(self):
        return self.blog_posts.filter(
            pub_date__lt = date.today()
        )

    def get_absolute_url(self):
        self.profile.get_absolute_url()

    def get_full_name(self):
        return self.profile.name
    
    def get_short_name(self):
        return self.profile.name