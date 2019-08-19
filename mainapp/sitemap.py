from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['sasv', 'contacts']

    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):

    def items(self):
        return Post.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.published_date