from bbstest1.apps.article import views
from django.views.static import serve
from django.conf import settings
from django.urls import path, re_path

app_name = 'article'
urlpatterns = [
    path(r'', views.ArticleListView.as_view(), name='index'),
    path(r'backend/', views.Backend.as_view(), name='backend'),
    path(r'add_article/', views.CreateArticleView.as_view(), name='add-article'),
    path(r'upload/', views.upload, name='attach-upload'),
    path(r'delete_article/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete-article'),
    path(r'edit_article/<int:pk>/', views.EditArticleView.as_view(), name='edit-article'),
    path(r'myarticle/<int:pk>/', views.MyArticle.as_view(), name='my-article'),
    path(r'updown/', views.updown, name='up-down'),
    path(r'comment/', views.comment, name='comment'),
    path(r'404/', views.page_not_find, name='404'),
    path(r'home/<str:username>/', views.HomePage.as_view(), name='homepage'),
]