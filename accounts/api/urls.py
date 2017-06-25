from django.conf.urls import url

from .views import (

		DriverListView,
		DriverDetailView
	)


urlpatterns=[


	url(r'^drivers$',DriverListView.as_view(),name='driver-list'),
	url(r'^drivers/(?P<pk>[\w-]+)/$',DriverDetailView.as_view(),name='driver-detail'),
]