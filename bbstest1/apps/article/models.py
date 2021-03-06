from django.db import models
from django.contrib.auth.models import AbstractUser
from bbstest1.apps.rbac.models import Role


class Blog(models.Model):
    """
    博客信息
    """
    # 个人博客主题
    title = models.CharField(max_length=64)
    # 博客主题
    theme = models.CharField(max_length=32)
    user = models.OneToOneField('accounts.UserInfo', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """
    个人博客文章分类
    """
    title = models.CharField(max_length=32)
    # 外间关联博客,一个博客站点可以关联多个分类
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.blog.title, self.title)

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    个人博客文章的标签
    """
    # 标签名字
    title = models.CharField(max_length=32)
    # 标签所属博客
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    个人博客的文章
    """
    title = models.CharField(max_length=50)  # 文章标题
    desc = models.CharField(max_length=255)  # 文章描述
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    category = models.ForeignKey(to="Category", null=True, on_delete=models.CASCADE)  # 文章分类
    user = models.ForeignKey(to='accounts.UserInfo', on_delete=models.CASCADE)  # 作者
    tags = models.ManyToManyField(  # 文章的标签
        to="Tag",
        through="Article2Tag",
        through_fields=('article', 'tag'),
    )
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    """
    文章详情表
    """
    content = models.TextField()  # 文章内容
    article = models.OneToOneField(to='Article', on_delete=models.CASCADE)

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = '文章详情'
        verbose_name_plural = verbose_name


class Article2Tag(models.Model):
    """
    文章和标签的多对多关系
    """
    article = models.ForeignKey(to="Article", on_delete=models.CASCADE)
    tag = models.ForeignKey(to="Tag", on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.article, self.tag)

    class Meta:
        unique_together = (('article', 'tag'),)
        verbose_name = '文章-标签'
        verbose_name_plural = verbose_name


class ArticleUpDown(models.Model):
    """
    点赞表
    """
    user = models.ForeignKey(to='accounts.UserInfo', null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article', null=True, on_delete=models.CASCADE)
    # 点赞或踩灭,True,赞,False,灭
    is_up = models.BooleanField(default=True)

    def __str__(self):
        return '{}-{}'.format(self.user_id, self.article_id)

    class Meta:
        # 同一个人只能给一篇文章点赞一次
        unique_together = (('article', 'user'),)
        verbose_name = '点赞'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    user = models.ForeignKey(to='accounts.UserInfo', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)

    # 自关联,自己给自己评论
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class School(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Order(models.Model):
    title = models.CharField(max_length=32)
    num = models.IntegerField()

    def __str__(self):
        return self.title
