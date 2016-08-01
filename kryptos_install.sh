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

#echo 'build finished, please add:'
#echo
#echo 'Alias /content/ ${cwd}/media/'
#echo 'Alias /media/ ${cwd}/venv/lib/python2.7/site-packages/django/contrib/admin/media/'
#echo 'WSGIScriptAlias / ${cwd}/kryptos.wsgi'
#echo 'WSGIRestrictStdin Off'
#echo
#echo 'to your httpd.conf and make sure that ${cwd} and ${cwd}/db are readable/writable by the webserver'
