#!/usr/bin/env python


        
d = 226
d_enc = 0
print d
for i in range(8):
	print "round %d: d mod 2:%d"%(i, d%2)
	if d % 2 == 1:
		d_enc+=1
	d = d >> 1
	if i != 7:
		d_enc = d_enc << 1

print d
print str(hex(d_enc))

for i in range(8):
	print "round %d: d_enc mod 2:%d"%(i, (d_enc>>i)%2)
