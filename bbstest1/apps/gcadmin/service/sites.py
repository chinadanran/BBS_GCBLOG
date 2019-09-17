from django.conf.urls import url
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from bbstest1.apps.gcadmin.mypage import Mypage
from django import forms
from django.db.models import Q
import copy
from django.forms.models import ModelChoiceField
from django.db.models.fields.related import ManyToManyField


class ModelStark(object):
    """
    默认配置类
    """
    model_form_class = []
    actions = []
    search_fields = []
    list_filter = []

    def patch_delete(self, request, queryset):
        '''
        批量删除函数
        :param request:
        :param queryset:
        :return: 无
        '''
        queryset.delete()

    patch_delete.desc = "批量删除"

    def get_url(self, obj, operating):
        '''
        反射url函数
        :param obj:当前的对象
        :param operating:反射方式，show，change，delete，
        :return:真是url
        '''
        if operating == 'change' or operating == 'delete':
            return reverse(self.model._meta.app_label + '_' + self.model._meta.model_name + '_' + operating,
                           args=(str(obj.pk),))
        return reverse(self.model._meta.app_label + '_' + self.model._meta.model_name + '_' + operating)

    def edit(self, obj=None, is_header=False):
        '''
        生成操作a标签函数
        :param obj:当前的对象
        :param is_header:是否是表头
        :return:
        '''
        if is_header:
            return "操作"
        return mark_safe(f"<a href='{self.get_url(obj,'change')}'>编辑</a>")

    def delete(self, obj=None, is_header=False):
        '''
        生成删除a标签函数
        :param obj: 当前的对象
        :param is_header: 是否是表头
        :return:
        '''
        if is_header:
            return "删除"
        return mark_safe(fr"<a href='{self.get_url(obj,'delete')}'>删除</a>")

    def checkbox(self, obj=None, is_header=False):
        '''
        生成选择a标签函数
        :param obj: 当前的对象
        :param is_header: 是否是表头
        :return:
        '''
        if is_header:
            return "选择"
        return mark_safe(f"<input type='checkbox' value={obj.pk}  name='pk_list'>")

    list_display = ['__str__']

    def __init__(self, model):
        self.model = model

    def get_new_actions(self):
        '''
        获取操作函数名与显示文字，加入默认的和自定义的批量操作
        :return:全部批量操作的列表[{'text':'显示文本','name}:'函数名字符串']
        '''
        temp = []
        temp.extend(self.actions)
        temp.append(self.patch_delete)
        new_actions = []
        for func in temp:
            new_actions.append({
                "text": func.desc,
                "name": func.__name__
            })
        return new_actions

    def get_search_condition(self, request):
        '''
        获取搜索条件进行Q的与操作筛选得到一个Q操作
        :param request:
        :return:Q操作条件
        '''
        val = request.GET.get("q")
        search_condition = Q()
        if val:
            search_condition.connector = "or"
            for field in self.search_fields:
                search_condition.children.append((field + "__icontains", val))

        return search_condition

    def get_list_filter_links(self, request):
        '''
        右侧筛选栏a标签拼接获得函数，首先遍历传入或默认的filter列表，得到需要过滤的字段名，
        再对GET请求过来的字典进行深度拷贝，继而request.GET这个字典就可以更改，从这个字典中取到需要字段pk值，通过get_field
        得到字段对象，字段对象.rel.to得到model类，通过model类得到全部对象，遍历这个queryset得到每个obj，如果obj.pk等于
        从GET请求中获取的pk值则在标签中多加个active 类。将所有标签加入列表中返回。
        :param request:
        :return:所有右侧筛选的a标签列表
        '''
        list_filter_links = {}
        for field in self.list_filter:
            params = copy.deepcopy(request.GET)
            current_filed_pk = params.get(field, 0)
            field_obj = self.model._meta.get_field(field)
            rel_model = field_obj.rel.to  # 通过字段对象得到model对象
            rel_model_queryset = rel_model.objects.all()
            temp = []
            for obj in rel_model_queryset:
                params[field] = obj.pk
                if obj.pk == int(current_filed_pk):
                    link = "<li class='active'><a href='?%s'>%s</a></li>" % (params.urlencode(), str(obj))
                else:
                    link = "<li><a href='?%s'>%s</a></li>" % (params.urlencode(), str(obj))
                temp.append(link)
            params.pop(field)
            temp.insert(0, "<li><a href='?%s'>ALL</a></li>" % (params.urlencode()))
            list_filter_links[field] = temp
        return list_filter_links

    def get_filter_condition(self, request):
        '''
         获取过滤条件进行Q的AND操作筛选得到一个Q条件
        :param request:
        :return: Q操作条件
        '''
        filter_condition = Q()
        for key, val in request.GET.items():
            if key in ["page", 'q']:
                continue
            filter_condition.children.append((key, val))
        return filter_condition

    def get_new_form(self, form):
        '''
        通过传入的form对象获取新的form对象函数：
        遍历传入的form，得到字段判断字段是否为ModelChoiceField(一对多，多对多)如果是的话，为其绑定一个is_pop属性为True，
        url = 通过当前字段对象得到的model对象的app名与类名反射出add_url，通过那个标签弹出的id，pop_back_id
        :param form:
        :return:新的form对象
        '''
        for bfield in form:
            if isinstance(bfield.field, ModelChoiceField):
                bfield.is_pop = True
                rel_model = self.model._meta.get_field(bfield.name).rel.to
                model_name = rel_model._meta.model_name
                app_label = rel_model._meta.app_label
                if app_label != 'auth':
                    _url = reverse("%s_%s_add" % (app_label, model_name))
                    bfield.url = _url
                    bfield.pop_back_id = "id_" + bfield.name
        return form

    def listview(self, request):
        '''
        视图函数：展示视图
        如果为POST请求时：则是复选框批量处理操作，首先获得全部需要批处理的所有主键值，得到所有对象，获取action（批处理函数名）
                          调用批处理函数，进行批处理
        如果为GET请求时： 1.首先取到所有需要展示的对象列表，然后得到search筛选条件和filter筛选条件，进行过滤，对过滤后的数据进行分页操作，
                          2.调用get_new_actions函数得到全部批处理操作和search_fields属性传到前端，
                          3.判断用户是否传入编辑与删除操作，如果没有就手动添加进入，并将checkbox也加入，
                          4.遍历默认或者用户传入的list_display列表，如果当前变量可以被调用则进行调用得到返回值添加到header_list中，
                                如果当前变量是__str__，将self.model._meta.model_name.upper()添加到header_list中，
                                其他则将self.model._meta.get_field(field_or_func).verbose_name添加到header_list中。
                                最后得到一个完整的表头列表。
                          5.遍历分页处理后的queryset，得到每个obj，然后遍历list_display得到要显示的表体内容，
                            判断当前变量是否可以被调用，如果可以则进行调用得到返回的安全处理过得a标签，
                            如果不可以则尝试获取当前model对象的当前字段对象，进而判断该字段是否为ManytoMany，如果是则取出str(全部对象)通过，连接返回
                            如果不是多对多字段直接获取内容添加到new_data_list中最后得到一个完整的表体列表
                          6.返回一个添加的a标签
        :param request:
        :return:
        '''
        if request.method == "POST":
            pk_list = request.POST.getlist("pk_list")
            queryset = self.model.objects.filter(pk__in=pk_list)
            action = request.POST.get("action")
            try:
                action = getattr(self, action)
                action(request, queryset)
            except:
                pass
        data_list = self.model.objects.all()
        search_condition = self.get_search_condition(request)
        filter_condition = self.get_filter_condition(request)
        get_list_filter_links = self.get_list_filter_links(request)
        data_list = data_list.filter(search_condition).filter(filter_condition)
        data_amount = data_list.count()
        page_num = request.GET.get('page', 1)
        page_obj = Mypage(page_num, data_amount, f'stark/{self.model._meta.app_label}/{self.model._meta.model_name}',
                          request, per_page_data=10)
        data = data_list[page_obj.ret_start: page_obj.ret_end]
        page_html = page_obj.ret_html()
        header_list = []
        get_new_actions = self.get_new_actions()
        search_fields = self.search_fields
        if ModelStark.edit not in self.list_display and ModelStark.delete not in self.list_display:
            self.list_display.extend((ModelStark.edit, ModelStark.delete))
            self.list_display.insert(0, ModelStark.checkbox)
        for field_or_func in self.list_display:
            if callable(field_or_func):
                val = field_or_func(self, is_header=True)
            else:
                if field_or_func == "__str__":
                    val = self.model._meta.model_name.upper()
                else:
                    val = self.model._meta.get_field(field_or_func).verbose_name
            header_list.append(val)
        new_data_list = []
        for obj in data:
            temp = []
            for field_or_func in self.list_display:
                if callable(field_or_func):
                    val = field_or_func(self, obj)
                else:
                    try:
                        field_obj = self.model._meta.get_field(field_or_func)
                        if isinstance(field_obj, ManyToManyField):
                            rel_data_list = getattr(obj, field_or_func).all()
                            l = [str(item) for item in rel_data_list]
                            val = ",".join(l)
                        else:
                            val = getattr(obj, field_or_func)
                    except Exception as e:
                        val = getattr(obj, field_or_func)
                temp.append(val)
            new_data_list.append(temp)
        add_url = self.get_url(None, 'add')
        return render(request, "utils/../templates/utils/list_view.html", locals())

    def get_model_form(self):
        '''
        得到一个model_form组件类,如果有传入的用传入的没有用默认的
        :return:
        '''
        if self.model_form_class:
            return self.model_form_class
        else:
            class ModelFormClass(forms.ModelForm):
                class Meta:
                    model = self.model
                    fields = "__all__"

            return ModelFormClass

    def addview(self, request):
        '''
        添加页面视图：首先获得当前的model_form类；
                      如果为POST请求：
                            实例化model_form，通过request.POST调用get_new_form方法得到一个新的form对象，对form进行验证，
                            通过验证后进行数据保存，获取是不是pop进行的POST请求，如果是获取保存导数据的内容的str与主键传入pop.html页面，
                            如果不是直接跳转到show展示页面。
                      如果为GET请求：
                            实例化model_form,通过form调用get_new_form方法得到一个新的form对象，render到add_view.html页面。
        :param request:
        :return:
        '''
        ModelFormClass = self.get_model_form()

        if request.method == "POST":
            form = ModelFormClass(request.POST)
            form = self.get_new_form(form)
            if form.is_valid():
                obj = form.save()
                is_pop = request.GET.get("pop")
                if is_pop:
                    text = str(obj)
                    pk = obj.pk
                    return render(request, "utils/../templates/utils/pop.html", locals())
                else:
                    return redirect(self.get_url(None, 'show'))
            return render(request, "utils/../templates/utils/add_view.html", locals())
        form = ModelFormClass()
        form = self.get_new_form(form)
        return render(request, "utils/../templates/utils/add_view.html", locals())

    def changeview(self, request, id):
        '''
        编辑页面视图：首先获得当前的model_form类，通过id过滤出需要编辑的对象；
              如果为POST请求：
                    实例化model_form，通过传入request.POST，和instance=编辑的对象实例出一个form对象调用get_new_form方法得到一个新的form对象，对form进行验证，
                    通过验证后进行数据保存，跳转到show展示页面。
              如果为GET请求：
                    实例化model_form,通过form调用get_new_form方法得到一个新的form对象，render到add_view.html页面。
        :param request:
        :param id:
        :return:
        '''
        ModelFormClass = self.get_model_form()
        edit_obj = self.model.objects.get(pk=id)
        if request.method == "POST":
            form = ModelFormClass(data=request.POST, instance=edit_obj)
            form = self.get_new_form(form)
            if form.is_valid():
                form.save()
                return redirect(self.get_url(edit_obj, 'show'))
            return render(request, "utils/../templates/utils/change_view.html", locals())
        form = ModelFormClass(instance=edit_obj)
        form = self.get_new_form(form)
        return render(request, "utils/../templates/utils/change_view.html", locals())

    def delview(self, request, id):
        '''
        删除视图函数：首先通过传入的id过滤选中的数据对象obj
                    如果为POST请求：
                                    对当前对象obj进行删除，返回show展示页面
                    如果为GET请求：
                                    反射获取show展示页面函数，返回确认删除页面del_view.html
        :param request:
        :param id:
        :return:
        '''
        obj = self.model.objects.filter(pk=id).first()
        if request.method == "POST":
            self.model.objects.filter(pk=id).delete()
            return redirect(self.get_url(obj, 'show'))
        list_url = self.get_url(obj, 'show')
        return render(request, "utils/../templates/utils/del_view.html", locals())

    def get_urls(self):
        temp = [
            url(r"^$", self.listview, name=f'{self.model._meta.app_label}_{self.model._meta.model_name}_show'),
            url(r"add/$", self.addview, name=f'{self.model._meta.app_label}_{self.model._meta.model_name}_add'),
            url(r"(\d+)/change/$", self.changeview,
                name=f'{self.model._meta.app_label}_{self.model._meta.model_name}_change'),
            url(r"(\d+)/delete/$", self.delview,
                name=f'{self.model._meta.app_label}_{self.model._meta.model_name}_delete'),
        ]
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


class AdminSite(object):
    """
    stark组件的全局类
    """

    def __init__(self):
        self._registry = {}

    def register(self, model, admin_class=None):
        if not admin_class:
            admin_class = ModelStark

        self._registry[model] = admin_class(model)

    def get_urls(self):
        temp = []
        for model, config_obj in self._registry.items():
            temp.append(url(r"%s/%s/" % (model._meta.app_label, model._meta.model_name), config_obj.urls))

        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


site = AdminSite()
