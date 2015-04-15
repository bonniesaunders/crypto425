from matmod import *
from polynomial import *

M = [ [1,0,0,0,1,1,1,1],
      [1,1,0,0,0,1,1,1],
      [1,1,1,0,0,0,1,1],
      [1,1,1,1,0,0,0,1],
      [1,1,1,1,1,0,0,0],
      [0,1,1,1,1,1,0,0],
      [0,0,1,1,1,1,1,0],
      [0,0,0,1,1,1,1,1] ] |mod| 2

p = Poly(0b100011011)

CV = [[1],[1],[0],[0],[0],[1],[1],[0]] |mod| 2


def reverse(L):
    return [ x for x in reversed(L) ]

def row(L):
    return [ [x for x in L] ]

def column(L):
    return [ [x] for x in L ] 

a = Poly(0b11111)
c = Poly(0b1100011)
mod = rijndael_poly()    
mod8 = Poly(0b100000001)

def q(x):
    return (a*x+c).MOD(mod8)

def SBox():
    for r in range(16):
        if r == 0: print [ q(0).hex]+[ q( Poly(r*16 + b).inverse(mod) ).hex.zfill(2) for b in range(1,16)]
        else: print [ q( Poly(r*16 + b).inverse(mod) ).hex.zfill(2) for b in range(16)]
    return 'done'
            
