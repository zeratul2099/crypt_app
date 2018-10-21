from django.conf.urls import url
from django.conf import settings
from django.views import static
from django.contrib import admin

from base_app import views as base_views
from hash import views as hash_views
from crypto import views as crypto_views


# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = [
    # Example:
    # (r'^sym_gui/', include('sym_gui.foo.urls')),
    url(r'^kryptos/$', base_views.base, name='base'),
    url(r'^kryptos/about/$', base_views.about, name='about'),
    url(r'^crypt_app/$', base_views.wrongUrl),
    url(r'^$', base_views.wrongUrl),
    url(r'^kryptos/info/(?P<algo>\w*)/(?P<page>\w*)/?$', base_views.info, name='info'),
    url(r'^kryptos/algo/hash/(?P<algo>\w*)/?$', hash_views.algo, name='hash_algo'),
    # (r'^kryptos/algo/stego/(?P<algo>\w*)/?$', stego_views.algo, name='stego_algo'),
    url(r'^kryptos/algo/crypto/(?P<algo>\w*)/?$', crypto_views.algo, name='crypto_algo'),
    # url(r'^kryptos/admin/(.*)$', admin.site.root),
    url(r'^content/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'^kryptos/(?P<algo_type>\w*)/$', base_views.list, name='list'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
]
