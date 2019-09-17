from bbstest1.apps.gcadmin.service.sites import site
from django.urls import path

app_name = 'gcadmin'
urlpatterns = [
    path(r'stark/', site.urls),
]