from django.conf.urls import patterns, url

from CalendarApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<poll_id>\d+)$', views.detail, name='detail'),
    url(r'^results/(?P<poll_id>\d+)$', views.results, name='results'),
    url(r'^vote/(?P<poll_id>\d+)$', views.vote, name='vote'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^register', views.register, name='register'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^changepassword', views.changepassword, name='changepassword'),
    url(r'^changeusername', views.changeusername, name='changeusername'),
    url(r'^ggmessage', views.ggmessage_view, name='ggmessage'),
)