from django.contrib import admin

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    # a tuple of field names to display, as columns on the change list page
    list_display = ('title', 'slug', 'first_created', 'pub_date', 'was_published_recently')

    # sidebar that lets people filter the change list by the pub_date field
    list_filter = ['pub_date']

    # add some search capability:
    search_fields = ['title']


class CommentAdmin(admin.ModelAdmin):
    # these will appear in the edit page and in this order
    fields = ('post', 'full_name', 'author_email', 'website', 'content')

    list_display = ('post', 'author_email', 'website', 'full_name', 'short_content')
    list_filter = ['post']
    search_fields = ['author_email', 'full_name']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
