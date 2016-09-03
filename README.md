# DEPRECATED
# check kryptos_install.sh for installation instructions
# TODO: rewrite


Kryptos
-------

System dependencies

- git
- python 3
- python virtualenv
- gcc
- (optional) nginx

Installation

create environment and checkout

`mkdir kryptos`

`cd kryptos`

`git clone https://github.com/zeratul2099/crypt_app.git`

`cd crypt_app`


use refactor branch

`git checkout refactor`


create virtual env

`pyenv venv`


activate virtual env

`source venv/bin/activate`


upgrade pip first

`pip install --upgrade pip`


install dependencies

`pip install django==1.9.8`

`pip install pycrypto==2.6.1`

`pip install uwsgi`


install m2crypto from git python3 branch

`cd venv`

`wget https://gitlab.com/m2crypto/m2crypto/repository/archive.tar.bz2?ref=python3 -O M2Crypto.tar.bz2`

`tar xjf M2Crypto.tar.bz2`

`cd m2crypto-python3-*`

`python setup.py build`

`python setup.py install`

`cd ..`

`rm -rf m2crypto-python3-*`


now you can start the testing development server with:

`PYTHONPATH=..:. DJANGO_SETTINGS_MODULE=crypt_app.settings django-admin runserver`


