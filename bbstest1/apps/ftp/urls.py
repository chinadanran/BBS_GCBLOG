from bbstest1.apps.ftp import views as f_view
from django.urls import path

app_name = 'ftp'
urlpatterns = [
    path(r'download/<str:path>', f_view.download, name='download'),
    path(r'del_file/<str:path>', f_view.del_file, name='del-file'),
    path(r'show-file/', f_view.show_file, name='show-file'),
    path(r'upload-file/', f_view.up_file, name='upload-file'),
]