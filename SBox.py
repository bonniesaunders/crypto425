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
    
