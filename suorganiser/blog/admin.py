from django.contrib import admin
from .models import Post
from django.db.models import Count
from datetime import datetime

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'tag_count')
    date_hierarchy = "pub_date"
    list_filter = ("pub_date",)
    ordering = ("title",)  
    prepopulated_fields = {"slug": ("title",)}

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.has_perm('blog.view_future_post'):
            queryset = queryset.filter(pub_date__lte = datetime.now())
        return queryset.annotate(
            tag_number = Count('tags'))

    def tag_count(self, post):
        return post.tag_number
    tag_count.short_description = 'Number of Tags'
    tag_count.admin_order_field = 'tag_number'

    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'author', 'text',
            )}
        ),
        ('Related', {
            'classes': (
                'wide',),
            'fields': (
                'tags', 'startups')
            }
        ),
    )
    filter_horizontal = ("startups", "tags")