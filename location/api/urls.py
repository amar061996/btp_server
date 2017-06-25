from django.conf.urls import url

from .views import LocationListView,LocationCreateView


urlpatterns=[

	url(r'^location/$',LocationListView.as_view(),name='list'),
	url(r'^create/$',LocationCreateView.as_view(),name='create'),
	
]