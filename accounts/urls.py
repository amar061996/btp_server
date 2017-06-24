from django.conf.urls import url
from django.contrib import admin


from django.conf import settings
from django.conf.urls.static import static

from accounts import views as account_views
urlpatterns = [
   
    url(r'^test/',account_views.test,name='test'),
]