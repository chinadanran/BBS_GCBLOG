"""bbstest1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.Login.as_view()),
    url(r'^check_v_code/', views.check_v_code),
    url(r'^v_code_img/', views.v_code_img),
    url(r'^registered/', views.registered),
    url(r'^check_email/', views.check_email),
    url(r'^check_phone/', views.check_phone),
    url(r'^check_username/', views.check_username),
    url(r'^check_showname/', views.check_showname),
    url(r'^check_password/', views.check_password),
    url(r'^index/', views.index),
    url(r'^backend/', views.backend),
    url(r'^add_article/', views.add_article),
    url(r'^upload/', views.upload),
    url(r'^delete_article/', views.delete_article),
    url(r'^edit_article/', views.edit_article),
    url(r'^myarticle/', views.myarticle),
    url(r'^logout/', views.logout_auth),
    url(r'^updown/', views.updown),
    url(r'^comment/', views.comment),
    url(r'^404/', views.page_not_find),
    url(r'^pcgetcaptcha/', views.pcgetcaptcha),
    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^home/(\w+)/$', views.home),
    url(r'^home/(\w+?)/(category|tag|archive)/(.*)/$', views.home),
]
