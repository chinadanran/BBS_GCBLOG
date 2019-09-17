#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "淡然"
# Date: 2018/9/5
from bbstest1.apps.accounts.models import UserInfo
from bbstest1.apps.article.models import *
from bbstest1.apps.gcadmin.service.sites import site


site.register(UserInfo)
site.register(Blog)
site.register(Category)
site.register(Tag)
site.register(Article)
site.register(ArticleDetail)
site.register(Article2Tag)
site.register(ArticleUpDown)
site.register(Comment)
site.register(School)
site.register(Order)
