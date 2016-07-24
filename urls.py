from django.conf.urls import patterns, url
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sym_gui/', include('sym_gui.foo.urls')),
    url(r'^kryptos/$', 'base_app.views.base'),
    url(r'^kryptos/about/$', 'base_app.views.about'),
    url(r'^crypt_app/$', 'base_app.views.wrongUrl'),
    url(r'^$', 'base_app.views.wrongUrl'),
    url(r'^kryptos/info/(?P<algo>\w*)/(?P<page>\w*)/?$', 'base_app.views.info'),        
    (r'^kryptos/algo/hash/(?P<algo>\w*)/?$', 'hash.views.algo'),
#    (r'^kryptos/algo/stego/(?P<algo>\w*)/?$', 'stego.views.algo'),
    (r'^kryptos/algo/crypto/(?P<algo>\w*)/?$', 'crypto.views.algo'),
#    url(r'^kryptos/admin/(.*)$', admin.site.root),
    url(r'^content/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'^kryptos/(?P<algo_type>\w*)/$', 'base_app.views.list', name='list'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
