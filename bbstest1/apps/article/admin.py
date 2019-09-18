from django.contrib import admin
from bbstest1.apps.article import models
from bbstest1.apps.gcadmin.service.sites import site

admin.site.register(models.Article)
admin.site.register(models.Article2Tag)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Blog)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.ArticleDetail)


site.register(models.Article)
site.register(models.Article2Tag)
site.register(models.Category)
site.register(models.Tag)
site.register(models.Comment)
site.register(models.Blog)
site.register(models.ArticleUpDown)
site.register(models.ArticleDetail)