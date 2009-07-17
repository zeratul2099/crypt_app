#!/usr/bin/env python

import os

for i in range(100):
    os.system("rasterizer -d png/absorb%d.png -snapshotTime %f absorb.svg"%(i, float(i)/4))
    os.chdir("png")
    os.system("convert -dispose previous -delay 10 -size 100x100 -geometry 800x800 -page +0+0 *.png animation.gif")

