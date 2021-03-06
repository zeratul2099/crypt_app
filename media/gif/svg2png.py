#!/usr/bin/env python

import os

name = "sha2_sigma1"

for i in range(0, 68, 2):
    os.system("rasterizer -d png/%s%3.3d.png -snapshotTime %f %s.svg &"%(name, i, float(i)/4, name))
    os.system("rasterizer -d png/%s%3.3d.png -snapshotTime %f %s.svg"%(name, i+1, float(i+1)/4, name))
os.chdir("png")
os.system("convert -dispose previous -delay 25 -page +0+0 %s*.png %s.gif"%(name, name))

