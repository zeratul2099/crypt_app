#!/bin/bash
PYTHONPATH=. DJANGO_SETTINGS_MODULE=settings poetry run django-admin runserver $@
