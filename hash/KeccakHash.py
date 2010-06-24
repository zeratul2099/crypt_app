#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with libstego.  If not, see <http://www.gnu.org/licenses/>.
#
#       Copyright 2009 2010 by Marko Krause <zeratul2099@googlemail.com>

import sys, os
import numpy as np
from KeccakState import KeccakState as State

class KeccakHash(object):
    #number of bytes per integer, on 32bit platforms this is 4
    num_b_i = 4
    r = 256
    rb = r/8
    ri = rb/num_b_i
    c = 544
    d = 28
    hash_len = 224
    num_rounds = 22

    def __init__(self, message):
        print message
        self.state = State(self.r, self.c, self.d, self.num_b_i, self.num_rounds, self.hash_len)
        self.absorb(self.state, message)
        self.squeeze(self.state)
        print self.state.digest
    
    def kezzak_f(self, state):
        # 22 rounds of kezzak
        for i in range(self.num_rounds):
            state.apply_theta()
            state.apply_chi()
            state.apply_pi()
            state.apply_rho()
            state.apply_iota(i)
        return state

    def absorb(self, state, message):
        print message
        message += '\x80'
        d_dec = state.d
        rb_dec = state.r / 8
        d_enc = 0
        rb_enc = 0
        # adding diversifier and r to message
        for i in range(8):
            if d_dec % 2:
                d_enc += 1
            if rb_dec % 2:
                rb_enc +=1
            if i != 7:
                d_dec = d_dec >> 1
                d_enc = d_enc << 1
                rb_dec = rb_dec >> 1
                rb_enc = rb_enc << 1
        message += chr(d_enc)
        message += chr(rb_enc)
        # filling message to a multipy of r
        to_fill = self.rb-(len(message)%self.rb)
        if to_fill > 0:
            message += '\x80'
            # filling 1 one and 7 zeros
            to_fill -= 1
            for i in range(to_fill):
                # filling 8 zeros
                message += '\0'
        num_p = (len(message)/self.rb)

        # iterate through message
        for p in range(num_p):
            # iterate through int in this block
            for i in range(self.ri):

                xor_byte = np.int32(0)
                for j in range(self.num_b_i):
                    if j != 0:
                        xor_byte = xor_byte << 8
                    try:
                        xor_byte ^= np.int32(ord(message[self.rb*p+self.num_b_i*i+(3-j)]))
                        
                    except:
                        xor_byte ^= 0
                state.state[i] ^= xor_byte
                    
            self.state = self.kezzak_f(self.state)

    def squeeze(self, state):
        if self.hash_len <= self.r:
           self.state.digest = np.uint32(self.state.state[0:7]) 

    def digest(self):
        return self.state.digest
    
    def hexdigest(self):
        hex_dig = ""
        for h in self.state.digest:
            hex_dig += hex(h).lstrip('0x').rstrip('L')
        return hex_dig
