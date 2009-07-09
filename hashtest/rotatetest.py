#!/usr/bin/env python


        
def mask(n):
    if n >= 0:
        return 2**n - 1
    else:
        return 0
 
def rol(n, rotations=1, width=32):
    rotations %= width
    if rotations < 1:
        return n
    n &= mask(width) ## Should it be an error to truncate here?
    return ((n << rotations) & mask(width)) | (n >> (width - rotations))
    
    
n=0x12345678
print hex(n)
n1 = rol(n, 14, 32)
print hex(n1)
print hex(rol(n1, 32-14, 32))



