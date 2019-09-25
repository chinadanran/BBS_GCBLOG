from django import forms
from django.core.validators import RegexValidator  # 导入Django内置的正则校验规则
from django.core.exceptions import ValidationError  # 导入Django内置的校验异常的类

from bbstest1.apps.accounts.models import UserInfo
from bbstest1.apps.article import models
import re


def user_check(value):
    user_obj = UserInfo.objects.filter(username=value)
    if user_obj:
        raise ValidationError("该用户名以被注册")
    else:
        return value


def email_check(value):
    user_obj = UserInfo.objects.filter(email=value)
    if user_obj:
        raise ValidationError("该邮箱以被注册")
    else:
        return value


def phone_check(value):
    user_obj = UserInfo.objects.filter(phone=value)
    if user_obj:
        raise ValidationError("该手机号码以被注册")
    else:
        return value


def pwd_check1(value):
    if not re.findall(r"[0-9]+", value):
        raise ValidationError("密码必须包含数字")
    else:
        return value


def pwd_check2(value):
    if not re.findall(r'[a-z]+', value):
        raise ValidationError("密码必须包含字母")
    else:
        return value


def pwd_check3(value):
    if not re.findall(r'([^a-z0-9A-Z])+', value):
        raise ValidationError("密码必须包含特殊字符")
    else:
        return value


class RegForm(forms.Form):
    email = forms.CharField(
        label='邮箱',
        validators=[RegexValidator(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', "邮箱格式不正确！"), email_check],
        error_messages={
            "required": "密码不能为空"
        },
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control", 'id': 'inputEmail3', 'placeholder': "需要通过邮件激活账户"}
        )
    )

    phone = forms.CharField(
        label='手机号码',
        error_messages={
            "required": "密码不能为空"
        },
        validators=[RegexValidator(r'(13|14|15|17|18|19)[0-9]{9}', "手机号码格式不正确！"), phone_check],
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control", 'style': "width: 100%", 'id': 'inputPhone', 'placeholder': "激活账户需要手机短信验证码"}
        )
    )

    username = forms.CharField(
        label='登录名称',
        error_messages={
            "required": "登录名不能为空"
        },
        validators=[RegexValidator(r'[A-Za-z0-9_\-\u4e00-\u9fa5]+', "登录名格式不正确！"), user_check],
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control", 'id': 'inputUserName', 'placeholder': "登录用户名，不少于4个字符"}
        )
    )

    name = forms.CharField(
        label='显示名称',
        error_messages={
            "required": "显示名不能为空"
        },
        validators=[RegexValidator(r'[A-Za-z0-9_\-\u4e00-\u9fa5]+', "显示名格式不正确！")],
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control", 'id': 'inputShowName', 'placeholder': "既昵称，不少于两个字符"}
        )
    )

    password = forms.CharField(
        min_length=8,
        max_length=15,
        label='密码',
        error_messages={
            "required": "密码不能为空",
            'min_length': '长度不能小于8位',
            'max_length': '长度不能大于15位',
        },
        validators=[pwd_check1, pwd_check2, pwd_check3],
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control", 'id': 'inputPassword3', 'placeholder': "至少8位，必须包含字母、数字、特殊字符"},
            render_value=True
        )
    )

    pwd_r_r = forms.CharField(
        min_length=8,
        max_length=15,
        label='确认密码',
        error_messages={
            "required": "密码不能为空",
            'min_length': '长度不能小于8位',
            'max_length': '长度不能大于15位',
        },
        validators=[pwd_check1, pwd_check2, pwd_check3],
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control", 'id': 'inputPassword2', 'placeholder': "请输入确认密码"},
            render_value=True
        )
    )
    avatar = forms.FileField(
        required=False,
        label='头像选择',
        widget=forms.widgets.FileInput(
            attrs={'accept': "image/*", 'style': "display: none;"},
        )
    )

    def clean(self):
        pwd = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("pwd_r_r")

        if re_pwd and re_pwd == pwd:
            return self.cleaned_data
        else:
            self.add_error('pwd_r_r', "两次密码不一致")
            raise ValidationError("两次密码不一致")
