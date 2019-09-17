from django.contrib import admin
from bbstest1.apps.article import models

admin.site.register(models.Article)
admin.site.register(models.Article2Tag)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Blog)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.ArticleDetail)