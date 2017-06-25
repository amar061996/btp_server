"""gpsmain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin


from django.conf import settings
from django.conf.urls.static import static

from location.api import urls as location_api_urls

from accounts.api import urls as accounts_api_urls

from accounts import views as account_views

from transport.api import urls as transport_api_urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',account_views.home,name='home'),
    url(r'^account/',include("accounts.urls",namespace='accounts')),
    url(r'^api/location/',include(location_api_urls,namespace='location-api')),
    url(r'^api/accounts/',include(accounts_api_urls,namespace='accounts-api')),
    url(r'^api/transport/',include(transport_api_urls,namespace='transport-api')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
