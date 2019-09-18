from bbstest1.apps.article import views
from django.views.static import serve
from django.conf import settings
from django.urls import path, re_path

app_name = 'article'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'backend/', views.backend, name='backend'),
    path(r'add_article/', views.add_article, name='add-article'),
    path(r'upload/', views.upload, name='attach-upload'),
    path(r'delete_article/', views.delete_article, name='delete-article'),
    path(r'edit_article/', views.edit_article, name='edit-article'),
    path(r'myarticle/', views.myarticle, name='my-article'),
    path(r'updown/', views.updown, name='up-down'),
    path(r'comment/', views.comment, name='comment'),
    path(r'404/', views.page_not_find, name='404'),
    path(r'home/<str:username>/', views.home, name='homepage'),
    path(r'home/<str:username>/<str:article_type>/<str:article_date>/', views.home, name='homepage-category'),
]