#!/bin/bash
PYTHONPATH=/var/www/kryptos/crypt_app:/var/www/kryptos DJANGO_SETTINGS_MODULE=crypt_app.settings django-admin runserver $@
