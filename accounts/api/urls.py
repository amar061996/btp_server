from django.conf.urls import url

from .views import (

		DriverListView,
		DriverDetailView,
		UserListView,
		UserDetailSerializer,
		UserContactView,
		UserContactCreateView
	)


urlpatterns=[

	################################################### DRIVERS URLS ###############################################################################

	url(r'^drivers$',DriverListView.as_view(),name='driver-list'),
	url(r'^drivers/(?P<pk>[\w-]+)/$',DriverDetailView.as_view(),name='driver-detail'),

	################################################### USERS URLS ###############################################################################
	url(r'^users$',UserListView.as_view(),name='users-list'),
	url(r'^users/(?P<username>[\w-]+)/$',UserDetailSerializer.as_view(),name='user-detail'),

	url(r'^users/contact/(?P<username>[\w-]+)/$',UserContactView.as_view(),name='user-contact-retrieve'),
	url(r'^users/create/contact/$',UserContactCreateView.as_view(),name='user-contact-create'),

]