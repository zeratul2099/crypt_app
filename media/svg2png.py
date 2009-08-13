#!/usr/bin/env python

import os

name = "lfsr"

for i in range(0, 101, 2):
    os.system("rasterizer -d png/%s%3.3d.png -snapshotTime %f %s.svg &"%(name, i, float(i)/5, name))
    os.system("rasterizer -d png/%s%3.3d.png -snapshotTime %f %s.svg"%(name, i+1, float(i+1)/5, name))
os.chdir("png")
os.system("convert -dispose previous -delay 20 -page +0+0 %s*.png %s.gif"%(name, name))

