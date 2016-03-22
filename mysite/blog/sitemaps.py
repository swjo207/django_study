from django.contrib.sitemaps import Sitemap
from .models import Post

# refer to(https://docs.djangoproject.com/en/1.8/ref/contrib/sitemaps/)
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self,obj):
        return obj.publish

