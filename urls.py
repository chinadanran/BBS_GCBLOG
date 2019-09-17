from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('bbstest1.apps.accounts.urls', namespace='accounts')),
]