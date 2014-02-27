from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^send/$', 'custom_user_auth.views.send'),
    url(r'^accounts/login/$', 'custom_user_auth.views.login'),
    url(r'^accounts/auth/$', 'custom_user_auth.views.auth_view'),
    url(r'^accounts/logout/$', 'custom_user_auth.views.logout'),
    url(r'^accounts/loggedin/$', 'custom_user_auth.views.loggedin'),
    url(r'^accounts/invalid/$', 'custom_user_auth.views.invalid_login'),

    url(r'^$', include('custom_user_auth.urls'), name='home'),
    # url(r'^custom_user/', include('custom_user.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
)
