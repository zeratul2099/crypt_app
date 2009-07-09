#!/usr/bin/env python
from KezzakHash import KezzakHash

filename = "views.pyc"
file = repr(open(filename, "rb").read())
kh = KezzakHash(file)
print kh.digest()
h = kh.hexdigest()
print h
print len(h)
