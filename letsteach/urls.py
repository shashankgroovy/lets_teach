from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$','django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'', include('accounts.urls')),
    url(r'', include('forum.urls')),
)

# the staticfiles_urlpatterns helper function will only work if DEBUG is True and the STATIC_URL
# setting is neither empty nor a full URL such as htp://static.example.com/

urlpatterns += staticfiles_urlpatterns()
