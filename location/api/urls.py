from django.conf.urls import url

from .views import LocationListView,LocationCreateView,UserLocationListView,UserLocationDetailView


urlpatterns=[

	url(r'^$',LocationListView.as_view(),name='list'),
	url(r'^create/$',LocationCreateView.as_view(),name='create'),
	url(r'^user/$',UserLocationListView.as_view(),name='user'),
	url(r'^user/(?P<username>[\w-]+)/$',UserLocationDetailView.as_view(),name='user-location-detail'),
]