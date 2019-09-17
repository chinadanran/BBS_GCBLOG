from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from bbstest1 import settings
from bbstest1.apps.article import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('bbstest1.apps.accounts.urls', namespace='accounts')),
    path('article/', include('bbstest1.apps.article.urls', namespace='article')),
    path('ftp/', include('bbstest1.apps.ftp.urls', namespace='ftp')),
    path('gcadmin/', include('bbstest1.apps.gcadmin.urls', namespace='gcadmin')),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
