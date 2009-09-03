from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sym_gui/', include('sym_gui.foo.urls')),
    (r'^crypt_app/$', 'base_app.views.base'),
    (r'^hash/$', 'hash.views.hash'),
    (r'^hash/algo/keccak/$', 'hash.views.algo_keccak'),
    (r'^hash/algo/md5/$', 'hash.views.algo_md5'),
    #(r'^hash/info/keccak/(?P<step>\w*)/?$', 'hash.views.info_keccak'),
    (r'^hash/info/(?P<algo>\w*)/(?P<page>\w*)/?$', 'hash.views.info'),
    #(r'^plist/(?P<customer_id>\d+)/$', 'plist.views.customerDetails'),
    (r'^hashtest/$', 'hashtest.views.hashtest'),
    (r'^admin/(.*)', admin.site.root),
    (r'^content/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
