from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django import views
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from bbstest1.apps.accounts.models import UserInfo
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from bbstest1.apps.article.forms import CreateArticleForm
from bbstest1.apps.article.models import Article, Comment, ArticleUpDown, ArticleDetail, Category
from bbstest1.apps.utils.mypage import Mypage
from django.db import transaction
from django.db.models import F, Q
import os
from django.conf import settings
from bs4 import BeautifulSoup


# 首页函数开始
class ArticleListView(ListView):
    model = Article
    paginate_by = 1
    ordering = 'create_time'
    template_name = 'index.html'
    extra_context = {
        'recommend_art_list': Article.objects.filter(up_count__gt=5),
    }


class MyArticle(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'myarticle.html'


def page_not_find(req):
    return render(req, '404.html')


class HomePage(ArticleListView):

    def get_queryset(self):
        query = Q(user__username__iexact=self.kwargs.get('username'))
        if self.request.GET:
            article_type = self.request.GET.get('type', '')
            article_date = self.request.GET.get('date', '')
            if article_type == "category":
                query = query & Q(category__title=article_date)
            elif article_type == "tag":
                query = query & Q(tags__title=article_date)
            else:
                try:
                    year, month = article_date.split("-")
                    query = query & Q(create_time__year=year, create_time__month=month)
                except Exception as e:
                    pass

        return Article.objects.filter(query)


@login_required
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


@login_required
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


class Backend(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 10
    ordering = 'create_time'
    template_name = 'backend.html'

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)


# 添加新文章
class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = 'add_article.html'
    form_class = CreateArticleForm
    success_url = reverse_lazy('article:backend')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'user': self.request.user})
        return form_class(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        ArticleDetail.objects.create(
            content=form.cleaned_data['content'],
            article=self.object
        )
        return HttpResponseRedirect(self.get_success_url())


# 富文本编辑器的图片上传
@login_required
def upload(request):
    res = {"error": 0}
    file_obj = request.FILES.get("imgFile")
    file_path = os.path.join(settings.MEDIA_ROOT, "article_imgs", file_obj.name)
    with open(file_path, "wb") as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    res["url"] = reverse_lazy('media', kwargs={'path': 'article_imgs\\' + file_obj.name})
    return JsonResponse(res)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('article:backend')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        ArticleDetail.objects.filter(article=self.object).filter().delete()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class EditArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    success_url = reverse_lazy('article:backend')
    template_name = 'edit_article.html'
    form_class = CreateArticleForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'user': self.request.user})
        return form_class(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        article_detail = ArticleDetail.objects.filter(article=self.object).first()
        article_detail.content=form.cleaned_data['content']
        article_detail.save()
        return HttpResponseRedirect(self.get_success_url())
