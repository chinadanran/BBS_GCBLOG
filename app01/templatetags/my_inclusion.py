from django import template
from app01 import models
from django.db.models import Count


register = template.Library()


@register.inclusion_tag(filename='left_menu.html')
def left_menu(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    category_list = models.Category.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)
    return {
        'user':user_obj,
        "category_list": category_list,
        "tag_list": tag_list,
    }


@register.inclusion_tag(filename='right_menu.html')
def right_menu(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    article_list = models.Article.objects.filter(user=user_obj)
    archive_list = models.Article.objects.filter(user=user_obj).extra(
        select={"y_m": "DATE_FORMAT(create_time, '%%Y-%%m')"}
    ).values("y_m").annotate(c=Count("id")).values("y_m", "c")
    return {
        'user':user_obj,
        'article_list':article_list,
        "archive_list": archive_list
    }