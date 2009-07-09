import numpy as np

class KezzakState(object):
    
    def __init__(self, r, c, d, num_b_i, num_rounds, hash_len):
        self.r = r
        self.c = c
        self.d = d
        self.state = np.int32([ 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, ])
        self.num_b_i = num_b_i
        self.hash_len = hash_len
        self.digest = np.int32([ 0 for x in range(r/(8*self.num_b_i)) ])
        # initate round constants according reference implementation
        self.round_const = np.uint32([0 for i in range(num_rounds)])
        LFSR = 0x01
        for i in range(num_rounds):
            # use 6 for 32bit-arch
            for j in range(6):
                bit_pos = (1 << j)-1
                result = self.LFSR86540(LFSR)
                LFSR = result[1]
                if result[0]:
                    self.round_const[i] ^= 1<<bit_pos

    def LFSR86540(self, LFSR):
        result = (LFSR & 0x01) != 0
        if (LFSR & 0x80) != 0:
            LFSR = ((LFSR << 1)-256) ^ 0x71
        else:
            LFSR = self.rol(LFSR, 1, 8)
        return [result, LFSR]
                
    def get_bit(self, x, y, z):
        int = self.state[5*(y%5)+(x%5)]
        int = int >> (z%(self.num_b_i*8))
        return (int & 0x0000001)
        
    def get_plane(self, y):
        return [ self.state[5*(y%5)],
                 self.state[5*(y%5)+1],
                 self.state[5*(y%5)+2],
                 self.state[5*(y%5)+3],
                 self.state[5*(y%5)+4], ]
                 
    def get_sheet(self, x):
        return [ self.state[(x%5)],
                 self.state[(x%5)+5],
                 self.state[(x%5)+10],
                 self.state[(x%5)+15],
                 self.state[(x%5)+20], ]
                 
    def get_lane(self, x, y):
        return self.state[5*(y%5)+(x%5)]
        
    def get_row(self, y, z):
        plane = self.get_plane(y%5)
        row = []
        for p in plane:
            row.append((p >> (z%(self.num_b_i*8))) & 0x0000001)
        return row
        
    def get_column(self, x, z):
        sheet = self.get_sheet(x%5)
        column = []
        for c in sheet:
            column.append((c >> (z%(self.num_b_i*8))) & 0x0000001)
        return column
        
    def set_lane(self, x, y, lane):
        self.state[5*(y%5)+(x%5)] = lane
        
    def set_plane(self, y, plane):
        for i in range(5):
            self.state[5*(y%5)+i] = plane[i]
            
    def set_sheet(self, x, sheet):
        for i in range(5):
            print self.state[(x%5)+(i*5)]
            self.state[(x%5)+(i*5)] = sheet[i]

    def set_bit(self, x, y, z, bit):
        lane = self.get_lane(x,y)
        bit = (bit%2) << (z%(self.num_b_i*8))
        mask = ~(1 << (z%(self.num_b_i*8)))
        lane &= mask
        lane |= bit
        self.set_lane(x, y, np.int32(lane))
        
    def set_row(self, y, z, row):
        for i in range(5):
            self.set_bit(i, y, z, row[i])
            
    def set_column(self, x, z, column):
        for i in range(5):
            self.set_bit(x, i, z, column[i])
            
    def mask(self, n):
        if n >= 0:
            return 2**n - 1
        else:
            return 0
 
    def rol(self, n, rotations=1, width=32):
        rotations %= width
        if rotations < 1:
            return n
        n &= self.mask(width)
        return ((n << rotations) & self.mask(width)) | (n >> (width - rotations))
    
    def rotate_lane(self, x, y, offset):
        offset = offset % (self.num_b_i*8)
        lane = self.get_lane(x, y)
        lane = np.int32(self.rol(lane, offset, self.num_b_i*8))
        self.set_lane(x, y, lane)
        
        

    def apply_chi(self):
        for x in range(5):
            for y in range(5):
                lane = self.get_lane(x, y)
                lane1 = self.get_lane(x+1, y)
                lane2 = self.get_lane(x+2, y)
                lane = lane ^ (~lane1 & lane2)
                self.set_lane(x, y, lane)
                
    def apply_theta(self):
        C = np.int32([0,0,0,0,0])
        D = np.int32([0,0,0,0,0])
        for x in range(5):
            C[x] = self.get_lane(x,0)
            for y in range(4):
                C[x] = C[x] ^ self.get_lane(x,y+1)
        for x in range(5):
            lane2 = C[(x+1)%5]
            if lane2 > 0x7fffffff:
                lane2 = (lane2 << 1)+1
            else:
                lane2 = lane2 << 1
            D[x] = C[(x-1)%5] ^ lane2
            for y in range(5):
                new_lane = self.get_lane(x,y) ^ D[x]
                self.set_lane(x,y, new_lane)
                
    def apply_pi(self):
        map =      [4, 19, 9, 24, 14,
                    18, 8, 23, 13, 3,
                    7, 22, 12, 2, 17,
                    21, 11, 1, 16, 6,
                    10, 0, 15, 5, 20, ]
        new_state = np.int32([ 0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0, ])
        for i in range(25):
            new_state[map[i]] = self.state[i]
        self.state = new_state
        
    def apply_rho(self):
        map = [ 153, 231, 3, 10, 171,
                55, 276, 36, 300, 6,
                28, 91, 0, 1, 190,
                120, 78, 210, 66, 253,
                21, 136, 105, 45, 15, ]
        for i in range(25):
            x = i%5
            y = i/5
            self.rotate_lane(x, y, map[i])
        
    def apply_iota(self, round):
        lane = self.get_lane(0,0)
        lane = np.int32(lane ^ self.round_const[round])
        self.set_lane(0, 0, lane)
        

