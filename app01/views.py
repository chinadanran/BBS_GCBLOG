from django.shortcuts import render, redirect, HttpResponse
from django import views
from app01 import models
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.http import JsonResponse
from app01.forms import RegForm
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from geetest import GeetestLib
from utils.mypage import Mypage
from django.db.models import Count

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# Create your views here.
# ==================================================
# 登录开始
class Login(views.View):

    def get(self, request):
        '''
        登录函数GET请求
        :param request:
        :return: login页面
        '''
        return render(request, 'login.html')

    def post(self, request):
        '''
        登录函数POST请求
        :param request:
        :return: 成功返回index页面，失败返回login页面
        '''
        data = {'count': 0}
        user_name = request.POST.get('email')
        pwd = request.POST.get('pass')
        user = authenticate(username=user_name, password=pwd)
        if user is None:
            data['user_msg'] = '用户名或密码错误'
            data['count'] = 1
        else:
            login(request, user)
            next_url = request.GET.get('next')
            request.session['user'] = user_name
            request.session['showname'] = models.UserInfo.objects.get(username=user).name
            if next_url and not request.path_info:
                rep = redirect(f'{next_url}')
                return rep
            else:
                return redirect('/index/')
        return render(request, 'login.html', data)


@never_cache
def v_code_img(request):
    '''
    生成验证码图片函数
    :param request:
    :return: 验证码图片数据data
    '''

    def random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),

    image_obj = Image.new(
        "RGB",
        (169, 34),
        random_color()
    )
    draw_obj = ImageDraw.Draw(image_obj)
    font_obj = ImageFont.truetype('static/fonts/alph.ttf', size=28)

    tmp = []
    for i in range(6):
        r = random.choice([str(random.randint(0, 9)), chr(random.randint(65, 90)), chr(random.randint(97, 122))])
        tmp.append(r)
        draw_obj.text(
            (i * 20 + random.randint(20, 30), random.randint(-4, 4)),
            r,
            fill=random_color(),
            font=font_obj
        )

    # 加干扰线
    width = 169  # 图片宽度（防止越界）
    height = 34
    for i in range(3):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=random_color())

    # 加干扰点
    for i in range(20):
        draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=random_color())

    v_code = "".join(tmp)
    request.session['v_code'] = v_code.upper()
    f = BytesIO()
    image_obj.save(f, "png")
    data = f.getvalue()
    return HttpResponse(data, content_type="image/png")


def check_v_code(request):
    '''
    验证码校验函数
    :param request:
    :return: Json数据包括验证状态和错误信息
    '''
    data = {'count': 0, 'error_msg': ''}
    v_code = request.POST.get('v_code')
    if v_code.upper() != request.session.get("v_code", ""):
        data['count'] = 1
        data['error_msg'] = '验证码输入错误'
    return JsonResponse(data)


def logout_auth(request):
    '''
    注销用户函数
    :param request:
    :return: 登录页面
    '''
    logout(request)
    return redirect("/login/")


# 登录结束
# ==================================================
# 注册开始
def registered(request):
    form_obj = RegForm()
    res = {'code': 0}
    if request.method == "POST":
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            form_obj = RegForm(request.POST, request.FILES)
            if form_obj.is_valid():
                form_obj.cleaned_data.pop('pwd_r_r')
                models.UserInfo.objects.create_user(**form_obj.cleaned_data)
                return redirect('/login/')
            else:
                return render(request, "registered.html", {"form_obj": form_obj})
        else:
            # 滑动验证码校验失败
            res["code"] = 1
            res["msg"] = "验证码错误"
            return JsonResponse(res)
    return render(request, "registered.html", {"form_obj": form_obj})


def check_email(req):
    if req.method == "POST":
        msg = {'count': 0, 'msg': ''}
        email = req.POST.get('email')
        if re.findall('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', email):
            obj_list = models.UserInfo.objects.filter(email=email)
            if obj_list:
                msg['count'] = 1
                msg['msg'] = '该邮箱已注册'
        else:
            msg['count'] = 1
            msg['msg'] = '邮箱格式不正确'
        return JsonResponse(msg)


def check_phone(req):
    if req.method == "POST":
        msg = {'count': 0, 'msg': ''}
        phone = req.POST.get('phone')
        if re.findall('(13|14|15|17|18|19)[0-9]{9}', phone):
            obj_list = models.UserInfo.objects.filter(phone=phone)
            if obj_list:
                msg['count'] = 1
                msg['msg'] = '手机号已被注册'
        else:
            msg['count'] = 1
            msg['msg'] = '手机号格式不正确'
        return JsonResponse(msg)


def check_username(req):
    if req.method == "POST":
        msg = {'count': 0, 'msg': ''}
        username = req.POST.get('username')
        if re.findall('[A-Za-z0-9_\-\u4e00-\u9fa5]+', username):
            obj_list = models.UserInfo.objects.filter(username=username)
            if obj_list:
                msg['count'] = 1
                msg['msg'] = '用户名已被注册'
        else:
            msg['count'] = 1
            msg['msg'] = '用户名格式不正确'
        return JsonResponse(msg)


def check_showname(req):
    if req.method == "POST":
        msg = {'count': 0, 'msg': ''}
        showName = req.POST.get('showName')
        if re.findall('[A-Za-z0-9_\-\u4e00-\u9fa5]+', showName):
            obj_list = models.UserInfo.objects.filter(name=showName)
            if obj_list:
                msg['count'] = 1
                msg['msg'] = '显示名已被注册'
        else:
            msg['count'] = 1
            msg['msg'] = '显示名格式不正确'
        return JsonResponse(msg)


def check_password(req):
    if req.method == "POST":
        password = req.POST.get('password')
        msg = {'count': 0, 'msg': ''}
        if len(password) != 0:
            if len(password) < 8:
                msg['count'] = 1
                msg['msg'] = '密码长度不足'
            msg['msg'] += ' 密码必须包含'
            if not re.findall(r"[0-9]+", password):
                msg['count'] = 1
                msg['msg'] += ' "数字"'

            if not re.findall(r'[a-z]+', password):
                msg['count'] = 1
                msg['msg'] += '"字母"'

            if not re.findall(r'([^a-z0-9A-Z])+', password):
                msg['count'] = 1
                msg['msg'] += '"特殊字符"'

        return JsonResponse(msg)


def pcgetcaptcha(request):
    '''
    滑动验证码校验函数
    :param request:
    :return:
    '''
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 注册函数结束
# ==========================================
# 首页函数开始
@login_required
def index(req):
    show_name = req.session.get('showname', '')
    article_list = models.Article.objects.all()
    data_amount = article_list.count()
    page_num = req.GET.get('page', 1)
    page_obj = Mypage(page_num, data_amount, 'index', per_page_data=5)
    data = article_list[page_obj.ret_start: page_obj.ret_end]
    page_html = page_obj.ret_html()
    recommend_art_list = models.Article.objects.filter(up_count__gt=5)
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
#     articles = models.Article.objects.filter(user__username=user)
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
        recommend_art_list = models.Article.objects.filter(up_count__gt=5)
        article_id = req.GET.get('article_id')
        article_obj = models.Article.objects.filter(id=article_id).first()
        contents = models.ArticleDetail.objects.filter(article_id=article_id).first().content
    except:
        return redirect('/404/')
    return render(req, 'myarticle.html',
                  {'contents': contents, 'article': article_obj, 'recommend_art_list': recommend_art_list})


def page_not_find(req):
    return render(req, '404.html')


def home(req, username, *args, **kwargs):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    article_list = models.Article.objects.filter(user=user_obj)
    my_article_list = article_list
    blog_obj = user_obj.blog
    category_list = models.Category.objects.filter(blog=blog_obj)
    tag_list = models.Tag.objects.filter(blog=blog_obj)
    archive_list = models.Article.objects.filter(user=user_obj).extra(
        select={"y_m": "strftime('%%Y-%%m',create_time,'localtime')"}
    ).values("y_m").annotate(c=Count("id")).values("y_m", "c")
    url = f'home/{username}'
    if args:
        url = f'home/{username}/{args[0]}/{args[1]}'
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
        "blog": blog_obj,
        "data": data,
        "my_article_list": my_article_list,
        "category_list": category_list,
        "tag_list": tag_list,
        "archive_list": archive_list,
        "user": user_obj,
        'page_html': page_html
    })
