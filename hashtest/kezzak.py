#!/usr/bin/env python
import sys, os
import numpy as np
from State import State
#number of bytes per integer, on 32bit platforms this is 4
num_b_i = 4
r = 224
rb = r/8
ri = rb/num_b_i
c = 576
d = 28
hash_len = 224
num_rounds = 18
filename = "views.pyc"
#filename = "test.pdf"

    
def kezzak_f(state):
    # 18 rounds of kezzak
    for i in range(num_rounds):
        state.apply_chi()
        state.apply_theta()
        state.apply_pi()
        state.apply_rho()
        state.apply_iota(i)
    return state

def absorb(state, message):
	message += '\x80'
	d_enc = 0
	for i in range(8):
		if d % 2:
			d_enc += 1
		if i != 7:
			d = d >> 1
			d_enc = d_enc << 1
    num_p = (len(message)/rb)+1
    if len(message)%rb == 0:
        num_p -= 1
    # iterate through message
    for p in range(num_p):
        # iterate through int in this block
        for i in range(ri):

            xor_byte = np.int32(0)
            for j in range(num_b_i):
                if j != 0:
                    xor_byte = xor_byte << 8
                try:
                    xor_byte ^= np.int32(ord(message[rb*p+num_b_i*i+(3-j)]))
                    
                except:
                    xor_byte ^= 0
            state.state[i] ^= xor_byte
                
        kezzak_f(state)

def squeeze(state):
    if hash_len <= r:
       state.digest = state.state[0:7] 
    #for z in range(hash_len/8)
    #pass

state = State(r, c, d, num_b_i, num_rounds, hash_len)
file = open(filename, "rb").read()
message = "Hello World! This is an test-message with Spam & Eggs and many vikings"
message ="\x01\x01"
#state.set_lane(3,3,0x12345678)
absorb(state, file)
squeeze(state)
print state.digest

