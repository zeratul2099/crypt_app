Kryptos
=======

[![Build Status](https://travis-ci.com/zeratul2099/crypt_app.svg?branch=master)](https://travis-ci.com/zeratul2099/crypt_app)

System dependencies
-------------------

- git
- python 3.5+
- poetry
- (optional) nginx

Installation
------------


    - git clone https://github.com/zeratul2099/crypt_app.git
    - cd crypt_app

    - pip install poetry
    - poetry install --no-dev



Django development server
-------------------------

Now you can start the testing development server with:

    PYTHONPATH=. DJANGO_SETTINGS_MODULE=settings poetry run django-admin runserver

or
    poetry run ./testserver.sh

Nginx configuration
-------------------

Add this to your nginx site config:


    upstream django {
        server 127.0.0.1:8000;
    }

    location /kryptos {
        uwsgi_pass django;
        include <crypt_app dir>/uwsgi_params;
    }

    location /content {
        alias <crypt_app dir>/media;
    }


and start the uswgi process with

    poetry run uwsgi --socket=127.0.0.1:8000 --module wsgi:application --master --vacuum --env PYTHONPATH=. --env DJANGO_SETTINGS_MODULE=settings -p 3

