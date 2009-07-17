#!/usr/bin/env python

import os

#for i in range(88):
#    os.system("rasterizer -d png/squeeze%2.2d.png -snapshotTime %f squeeze.svg"%(i, float(i)/4))
os.chdir("png")
os.system("convert -dispose previous -delay 25 -geometry 600x600 -page +0+0 *.png animation.gif")

