#!/usr/bin/env python

import os

for i in range(100):
    os.system("rasterizer -d png/absorb%2.2d.png -snapshotTime %f absorb.svg"%(i, float(i)/4))
os.chdir("png")
os.system("convert -dispose previous -delay 25 -page +0+0 absorb*.png animation.gif")

