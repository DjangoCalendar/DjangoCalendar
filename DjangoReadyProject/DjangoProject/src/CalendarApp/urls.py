from django.conf.urls import patterns, url
from django.conf import settings
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
    url(r'^ggmessage', views.ggmessage_view, name='ggmessage'),
    url(r'^accountdetails', views.accountdetails, name='accountdetails'),
    url(r'^year/(\d+)/$', 'CalendarApp.views.main'),
    url(r'^year', 'CalendarApp.views.main'),
    url(r'^month/(\d+)/(\d+)/(prev|next)/$', 'CalendarApp.views.month'),
    url(r'^month/(\d+)/(\d+)/$', 'CalendarApp.views.month'),
    url(r'^month/$', 'CalendarApp.views.month'),
    url(r'^day/(\d+)/(\d+)/(\d+)/$', 'CalendarApp.views.day'),
    url(r'^settings/$', 'CalendarApp.views.settings'),
	url(r'^startthread', views.startthread, name='startthread'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        })
)

#if settings.DEBUG:
#    urlpatterns += patterns('',
#        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.MEDIA_ROOT,
#        }),
#)