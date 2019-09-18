from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from bbstest1 import settings
from bbstest1.apps.article import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('bbstest1.apps.accounts.urls', namespace='accounts')),
    path('article/', include('bbstest1.apps.article.urls', namespace='article')),
    path('ftp/', include('bbstest1.apps.ftp.urls', namespace='ftp')),
    path('gcadmin/', include('bbstest1.apps.gcadmin.urls', namespace='gcadmin')),
    path(r'media/<str:path>', serve, {"document_root": settings.MEDIA_ROOT}, name='media'),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
