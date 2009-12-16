from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sym_gui/', include('sym_gui.foo.urls')),
    (r'^kryptos/$', 'base_app.views.base'),
    (r'^kryptos/about/$', 'base_app.views.about'),
    (r'^crypt_app/$', 'base_app.views.wrongUrl'),
    (r'^$', 'base_app.views.wrongUrl'),
    (r'^kryptos/info/(?P<algo>\w*)/(?P<page>\w*)/?$', 'base_app.views.info'),        
    (r'^kryptos/hash/algo/(?P<algo>\w*)/?$', 'hash.views.algo'),
    (r'^kryptos/stego/algo/(?P<algo>\w*)/?$', 'stego.views.algo'),
    (r'^kryptos/crypto/algo/(?P<algo>\w*)/?$', 'crypto.views.algo'),
    (r'^kryptos/admin/(.*)', admin.site.root),
    (r'^content/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^kryptos/(?P<algo_type>\w*)/$', 'base_app.views.list'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
