from django.contrib import admin
from bbstest1.apps.accounts import views
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path(r'login/', views.Login.as_view(), name='login'),
    path(r'admin/', admin.site.urls),
    path(r'pcgetcaptcha/', views.pcgetcaptcha, name='pcgetcaptcha'),
    path(r'check_v_code/', views.check_v_code, name='check-v-code'),
    path(r'v_code_img/', views.v_code_img, name='code-img'),
    path(r'registered/', views.registered, name='registered'),
    path(r'check_email/', views.check_email, name='check-email'),
    path(r'check_phone/', views.check_phone, name='check-phone'),
    path(r'check_username/', views.check_username, name='check-username'),
    path(r'check_showname/', views.check_showname, name='check-showname'),
    path(r'check_password/', views.check_password, name='check-password'),
    path(r'logout/', views.logout_auth, name='logout'),
]
