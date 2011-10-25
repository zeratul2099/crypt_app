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

#git clone git://gitorious.org/kryptos/crypt_app.git


cwd = `pwd`
virtualenv --no-site-packages --python=python2.7 venv
echo 'virtualenv created. Use it by executing "source venv/bin/activate"'
#pip:
#----
source venv/bin/activate
pip install django==1.2
pip install pycrypto==2.4
pip install m2crypto==0.21.1 --no-install
cp remove-sslv2.patch venv/build/m2crypto
cd venv/build/m2crypto
patch -p0 < remove-sslv2.patch
python setup.py build
python setup.py install
cd ../../../../
git clone git://gitorious.org/libstego/libstego.git
cd libstego
cmake -DPYTHON_LIBRARY=~/code/kryptos/venv/include/python2.7 -DCMAKE_CXX_COMPILER=gcc .
make
cp swig_bindings/_libstego* ../crypt_app/stego/
cp swig_bindings/libstego*.py ../crypt_app/stego/
cp src/libstego/libstego.so ../crypt_app/
cp src/libstegofile/libstegofile.so ../crypt_app/

echo 'build finished, please add:'
echo
echo 'Alias /content/ ${cwd}/media/'
echo 'Alias /media/ ${cwd}/venv/lib/python2.7/site-packages/django/contrib/admin/media/'
echo 'WSGIScriptAlias / ${cwd}/kryptos.wsgi'
echo 'WSGIRestrictStdin Off'
echo
echo 'to your httpd.conf and make sure that ${cwd} and ${cwd}/db are readable/writable by the webserver'