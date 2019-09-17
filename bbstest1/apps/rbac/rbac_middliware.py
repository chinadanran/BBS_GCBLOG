#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "淡然"
# Date: 2018/9/5

from django.shortcuts import HttpResponse, render, redirect
from django.utils.deprecation import MiddlewareMixin
import re


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_path = request.path
        white_url = ["/login/", "/index/", "/admin/.*"]
        for reg in white_url:
            ret = re.search(reg, current_path)
            if ret:
                return None
        user = request.session.get("user")
        if not user:
            return reverse_lazy('accounts:login')
        permission_list = request.session.get("permission_list")
        for reg in permission_list:
            reg = "^%s$" % reg
            ret = re.search(reg, current_path)
            if ret:
                return None
        return HttpResponse("无权限访问！")