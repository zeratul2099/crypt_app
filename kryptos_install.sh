#!/bin/bash
#pre:
#----
#git
#python-virtualenv
#gcc
#python-dev
#swig
#cmake
#apache2
#libapache2-mod-wsgi

# git clone https://github.com/zeratul2099/crypt_app.git

cwd=`pwd`
# cleaning up first
rm -rf venv/
pyvenv venv

echo 'virtualenv created. Use it by executing "source venv/bin/activate"'
source venv/bin/activate

# upgrade pip first
pip install --upgrade pip

pip install django==1.9.8
pip install pycrypto==2.6.1
pip install uwsgi

# m2crypto from git python3 branch
cd venv
wget https://gitlab.com/m2crypto/m2crypto/repository/archive.tar.bz2?ref=python3 -O M2Crypto.tar.bz2
tar xjf M2Crypto.tar.bz2
cd m2crypto-python3-*
python setup.py build
python setup.py install
cd ..
rm -rf m2crypto-python3-*

#git clone https://github.com/zeratul2099/libstego.git
#cd libstego
#cmake -DPYTHON_LIBRARY=$cwd/venv/include/python2.7 -DCMAKE_CXX_COMPILER=gcc .
#make
#cp swig_bindings/_libstego* ../../stego/
#cp swig_bindings/libstego*.py ../../stego/
#cp src/libstego/libstego.so ../../
#cp src/libstegofile/libstegofile.so ../../

# nginx configuration
echo 'build finished, please add:'
echo
echo 'location /kryptos {'
echo '	uwsgi_pass django;'
echo '	include ${cwd}/uwsgi_params;'
echo ''
echo ''
echo '}'
echo ''
echo 'location /content {'
echo '	alias ${cwd}/media;'
echo '}'

echo
echo 'and start the uswgi process with'
echo
echo 'uwsgi --socket=127.0.0.1:8000 --module wsgi:application --home=${cwd}/venv --master --vacuum --env PYTHONPATH=..:. --env DJANGO_SETTINGS_MODULE=crypt_app.settings -p 3'

echo 'from your virtual env'
