from django.shortcuts import render, redirect, HttpResponse
from django import views
from django.urls import reverse_lazy

from bbstest1.apps.accounts.models import UserInfo
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from bbstest1.apps.article.models import Article, Comment, ArticleUpDown, ArticleDetail, Category
from bbstest1.apps.utils.mypage import Mypage
from django.db import transaction
from django.db.models import F
import os
from django.conf import settings
from bs4 import BeautifulSoup


# 注册函数结束
# ==========================================
# 首页函数开始
def index(req):
    show_name = req.session.get('showname', '')
    article_list = Article.objects.all()
    data_amount = article_list.count()
    page_num = req.GET.get('page', 1)
    page_obj = Mypage(page_num, data_amount, 'index', per_page_data=5)
    data = article_list[page_obj.ret_start: page_obj.ret_end]
    page_html = page_obj.ret_html()
    recommend_art_list = Article.objects.filter(up_count__gt=5)
    return render(req, 'index.html', {'showname': show_name, 'article_list': data, 'page_html': page_html,
                                      'recommend_art_list': recommend_art_list})


# 首页函数结束
# ===================================================================
# 我的博园开始
# @login_required
# def myblog(req):
#     '''
#     我的博园函数
#     :param req:
#     :return: 我的博园页面
#     '''
#     user = req.session.get('user', '')
#     articles = Article.objects.filter(user__username=user)
#     data_amount = articles.count()
#     page_num = req.GET.get('page', 1)
#     page_obj = Mypage(page_num, data_amount, 'myblog', per_page_data=3)
#     data = articles[page_obj.ret_start: page_obj.ret_end]
#     page_html = page_obj.ret_html()
#     year_month = set()  # 设置集合，无重复元素
#     for a in articles:
#         year_month.add((a.create_time.year, a.create_time.month))  # 把每篇文章的年、月以元组形式添加到集合中
#     counter = {}.fromkeys(year_month, 0)  # 以元组作为key，初始化字典
#     for a in articles:
#         counter[(a.create_time.year, a.create_time.month)] += 1  # 按年月统计文章数目
#     year_month_number = []  # 初始化列表
#     for key in counter:
#         year_month_number.append([key[0], key[1], counter[key]])  # 把字典转化为（年，月，数目）元组为元素的列表
#     year_month_number.sort(reverse=True)  # 排序
#
#     return render(req, 'myblog.html',
#                   {'articleList': data, 'page_html': page_html, 'year_month_number': year_month_number})

def myarticle(req):
    '''
    我的文章函数
    :param req:
    :return: 文章页面
    '''
    try:
        article_id = req.GET.get('article_id')
        article_obj = Article.objects.filter(id=article_id).first()
        username = UserInfo.objects.filter(id=article_obj.user_id).first().username
        comment_list = Comment.objects.filter(article=article_obj)
    except:
        return redirect(reverse_lazy('article:404'))
    return render(req, 'myarticle.html', {'article': article_obj, 'username': username, 'comment_list': comment_list})


def page_not_find(req):
    return render(req, '404.html')


@login_required
def home(req, username, *args, **kwargs):
    '''
    个人博园站点函数
    :param req:
    :param username:
    :param args:
    :param kwargs:
    :return: 个人博园页面
    '''
    user_obj = UserInfo.objects.filter(username=username).first()
    article_list = Article.objects.filter(user=user_obj)
    url = 'home/{}'.format(username)
    if args:
        url = 'home/%s/%s/%s' % (username, args[0], args[1])
        if args[0] == "category":
            article_list = article_list.filter(category__title=args[1])
        elif args[0] == "tag":
            article_list = article_list.filter(tags__title=args[1])
        else:
            try:
                year, month = args[1].split("-")
                article_list = article_list.filter(create_time__year=year, create_time__month=month)
            except Exception as e:
                pass
    data_amount = article_list.count()
    page_num = req.GET.get('page', 1)
    page_obj = Mypage(page_num, data_amount, url, per_page_data=3)
    data = article_list[page_obj.ret_start: page_obj.ret_end]
    page_html = page_obj.ret_html()
    return render(req, "home.html", {
        'username': username,
        "data": data,
        'page_html': page_html
    })


def updown(request):
    if request.method == "POST":
        res = {"code": 0}
        user_id = request.POST.get("userId")
        article_id = request.POST.get("articleId")
        is_up = True if request.POST.get("isUp").upper() == 'TRUE' else False
        article_obj = Article.objects.filter(id=article_id, user_id=user_id)
        if article_obj:
            res["code"] = 1
            res["msg"] = '不能给自己的文章点赞！' if is_up else '不能反对自己的内容！'
        else:
            is_exist = ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first()
            if is_exist:
                if is_exist.is_up == is_up:
                    res["code"] = 2
                    res["msg"] = '已经取消点赞' if is_exist.is_up else '已经取消反对'
                    with transaction.atomic():
                        is_exist.delete()
                        Article.objects.filter(id=article_id).update(
                            up_count=F('up_count') - 1) if is_up else Article.objects.filter(
                            id=article_id).update(
                            down_count=F('down_count') - 1)
                else:
                    res['code'] = 1
                    res['msg'] = '已经点过赞' if is_exist.is_up else '已经反对过'
            else:
                with transaction.atomic():
                    ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
                    Article.objects.filter(id=article_id).update(
                        up_count=F('up_count') + 1) if is_up else Article.objects.filter(id=article_id).update(
                        down_count=F('down_count') + 1)
                res["msg"] = '点赞成功' if is_up else '反对成功'
        return JsonResponse(res)


def comment(request):
    rep = {}
    if request.method == 'POST':
        content = request.POST.get('content')
        article_id = request.POST.get('article')
        parent_id = request.POST.get('parent_id')
        parent_id = parent_id if parent_id else None
        with transaction.atomic():
            comment_obj = Comment.objects.create(article_id=article_id, user=request.user, content=content,
                                                        parent_comment_id=parent_id)
            Article.objects.filter(id=article_id).update(comment_count=F('comment_count') + 1)
            article_obj = Article.objects.filter(id=article_id).first()

            if comment_obj.parent_comment:
                rep['parent_comment'] = 0
                rep['parent_name'] = comment_obj.parent_comment.user.username
                rep['parent_content'] = comment_obj.parent_comment.content
            else:
                rep['parent_comment'] = 1
            rep['content'] = content
            rep['comment_id'] = comment_obj.id
            rep['comment_count'] = article_obj.comment_count
            rep['username'] = request.user.username
            rep['create_time'] = comment_obj.create_time.strftime('"%Y-%m-%d %H:%M"')
            rep['avatar'] = str(UserInfo.objects.filter(username=request.user.username).first().avatar)
    return JsonResponse(rep)


# 管理后台
@login_required
def backend(request):
    # 现获取当前用户的所有文章
    article_list = Article.objects.filter(user=request.user)
    return render(request, "backend.html", {"article_list": article_list})


# 添加新文章
@login_required
def add_article(request):
    if request.method == "POST":
        # 获取用户填写的文章内容
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")

        # 清洗用户发布的文章的内容，去掉script标签
        soup = BeautifulSoup(content, "html.parser")
        script_list = soup.select("script")
        for i in script_list:
            i.decompose()

        # 写入数据库
        with transaction.atomic():
            # 1. 先创建文章记录
            article_obj = Article.objects.create(
                title=title,
                desc=soup.text[0:150],
                user=request.user,
                category_id=category_id
            )
            # 2. 创建文章详情记录
            ArticleDetail.objects.create(
                content=soup.prettify(),
                article=article_obj
            )
        return redirect(reverse_lazy('article:backend'))

    # 把当前博客的文章分类查询出来
    category_list = Category.objects.filter(blog=request.user.blog)
    return render(request, "add_article.html", {"category_list": category_list})


# 富文本编辑器的图片上传
def upload(request):
    res = {"error": 0}
    file_obj = request.FILES.get("imgFile")
    file_path = os.path.join(settings.MEDIA_ROOT, "article_imgs", file_obj.name)
    with open(file_path, "wb") as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    # url = settings.MEDIA_URL + "article_imgs/" + file_obj.name
    url = "/media/article_imgs/" + file_obj.name
    res["url"] = url
    return JsonResponse(res)


@login_required
def delete_article(request):
    del_id = request.GET.get('del_id')
    article_obj = Article.objects.filter(id=del_id).first()
    if article_obj:
        with transaction.atomic():
            article_det_obj = ArticleDetail.objects.filter(article_id=del_id).filter().delete()
            article_obj.delete()
    else:
        return redirect(reverse_lazy('article:404'))
    return redirect(reverse_lazy('article:backend'))


@login_required
def edit_article(request):
    edit_id = request.GET.get('edit_id')
    article_list = Article.objects.filter(id=edit_id)
    article_obj = article_list.first()
    article_detile_list = ArticleDetail.objects.filter(article=article_obj)
    category_list = Category.objects.filter(blog=request.user.blog)
    if article_obj and article_detile_list:
        if request.method == 'POST':
            title = request.POST.get("title")
            content = request.POST.get("content")
            category_id = request.POST.get("category")

            soup = BeautifulSoup(content, "html.parser")
            script_list = soup.select("script")
            for i in script_list:
                i.decompose()
            with transaction.atomic():
                article_list.update(
                    title=title,
                    desc=soup.text[0:150],
                    user=request.user,
                    category_id=category_id
                )
                article_detile_list.update(
                    content=soup.prettify(),
                    article=article_obj
                )
            return redirect(reverse_lazy('article:backend'))

        content = ArticleDetail.objects.filter(article=article_obj).first().content
        return render(request, 'edit_article.html', locals())
    else:
        return redirect(reverse_lazy('article:404'))
