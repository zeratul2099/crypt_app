#!/usr/bin/env python

import os

name = "chi"

for i in range(360):
    os.system("rasterizer -d png/%s%3.3d.png -snapshotTime %f %s.svg"%(name, i, float(i)/4, name))
os.chdir("png")
os.system("convert -dispose previous -delay 25 -page +0+0 %s*.png %s.gif"%(name, name))

