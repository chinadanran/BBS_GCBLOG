from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11,null=True)
    avatar = models.FileField(upload_to='avatars/',default='avatars/dafault.pan')
    # blog = models.OneToOneField(to='Article',null=True)


    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    the_classification = models.ForeignKey(to='Classification')
    the_labels = models.ManyToManyField(to='Label')
    the_user = models.ForeignKey(to='UserInfo')


class Comment(models.Model):
    content = models.TextField()
    the_article = models.ForeignKey(to='Article')
    the_user = models.ForeignKey(to='UserInfo')


class GiveUpDown(models.Model):
    is_up = models.BooleanField(False)
    is_down = models.BooleanField(False)
    the_article = models.ForeignKey(to='Article')
    the_user = models.OneToOneField(to='UserInfo')


class Theme(models.Model):
    name = models.CharField(max_length=64)
    css_content = models.TextField()
    the_user = models.OneToOneField(to='UserInfo')


class Classification(models.Model):
    name = models.CharField(max_length=64)
    the_user = models.ForeignKey(to='UserInfo')


class Label(models.Model):
    name = models.CharField(max_length=64)
    the_user = models.ForeignKey(to='UserInfo')
