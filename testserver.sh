#!/bin/bash
PYTHONPATH=.. DJANGO_SETTINGS_MODULE=crypt_app.settings django-admin runserver $@
