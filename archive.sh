#!/bin/bash

git archive --output=../crypt_app.tar master
cd ..
bzip2 crypt_app.tar
exit 0
