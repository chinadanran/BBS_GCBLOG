#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "淡然"
# Date: 2018/9/5
from bbstest1.apps.gcadmin.service.sites import site
from bbstest1.apps.rbac.models import Role, Permission

site.register(Role)
site.register(Permission)
