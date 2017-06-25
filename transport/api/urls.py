from django.conf.urls import url

from .views import TransportListView,TransportDetailView


urlpatterns=[

	url(r'^$',TransportListView.as_view(),name="transport-list"),
	url(r'^(?P<pk>[\w-]+)/$',TransportDetailView.as_view(),name='transport-detail'),


]