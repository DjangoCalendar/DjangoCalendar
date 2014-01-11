from django.conf.urls import patterns, url

from CalendarApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<poll_id>\d+)$', views.detail, name='detail'),
    url(r'^results/(?P<poll_id>\d+)$', views.results, name='results'),
    url(r'^vote/(?P<poll_id>\d+)$', views.vote, name='vote'),
)