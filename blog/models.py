import datetime
from django.core.urlresolvers import reverse

from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(editable=False, max_length=200, unique=True)
    author = models.CharField(max_length=200)
    author_email = models.EmailField(max_length=254)
    summary = models.CharField(max_length=500)
    content = models.TextField()
    first_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    author_email = models.EmailField(max_length=254)
    website = models.URLField(blank=True, default='#', max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    # shorten the comment content for the admin change list page
    def short_content(self):
        return self.content[:20] + '...'

    short_content.short_description = 'Comments'

    def __str__(self):
        return self.content
