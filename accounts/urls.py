from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'accounts.views.index', name='index'),
    url(r'^signup/$', 'accounts.views.signup', name='signup'),
    url(r'^newsfeed/$', 'accounts.views.newsfeed', name='newsfeed'),
    url(r'^messagepost/$', 'accounts.views.message_post', name='message_post'),
    url(r'^users/$', 'accounts.views.users', name='users'),
    url(r'^follow/$', 'accounts.views.follow', name='follow'),
)
