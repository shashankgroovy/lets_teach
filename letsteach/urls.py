from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^register/', ".views.AccountRegistration"),
    #url(r'^login/$', "accounts.views.LoginRequest"),
    #url(r'^logout/$', "accounts.views.LogoutRequest"),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$','django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)

# this helper function will only work if DEBUG is True and the STATIC_URL
# setting is neither empty nor a full URL such as htp://static.example.com/

urlpatterns += staticfiles_urlpatterns()
