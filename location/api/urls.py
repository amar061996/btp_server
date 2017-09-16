from django.conf.urls import url

from .views import (
	LocationListView,
	LocationCreateView,
	UserLocationListView,
	UserLocationDetailView,
	TransportLocationListView,
	TransportLocationDetailView,
	TransportNearbyView,
	)


urlpatterns=[

	url(r'^$',LocationListView.as_view(),name='list'),
	url(r'^create/$',LocationCreateView.as_view(),name='create'),
	url(r'^user/$',UserLocationListView.as_view(),name='user'),
	url(r'^user/(?P<username>[\w-]+)/$',UserLocationDetailView.as_view(),name='user-location-detail'),
	url(r'^transport/$',TransportLocationListView.as_view(),name='transport'),
	url(r'^transport/(?P<pk>\d+)/$',TransportLocationDetailView.as_view(),name='transport-location-detail'),
	url(r'^nearby/(?P<username>[\w-]+)/$',TransportNearbyView.as_view(),name='transport-nearby'),
	

]