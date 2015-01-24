from matmod import *
from cypari.gen import pari
from math import sqrt
from random import randint

##It may be a long time before you find a perfect square,
##fermat_factorization may not stop.

def fermat_factorization(n):
    perfectsquare = False
    i = -1
    while not perfectsquare and i<n:
        i += 1
        h = n + i**2
        if ( h % 16 ) in [0,1,4,9]:
            perfectsquare = testsquare(h)
    return perfectsquare, int(sqrt(h))-i, int(sqrt(h)+i)
        
def testsquare(h):
    return int(sqrt(h))**2 == h
    
def UEF(n,k,m,a):
    b = a**m
    if b == 1 |mod| n: return 'try another a'
    for i in range(k):
        b1 = b**2
#        print i,b1
        if b1 == 1 |mod| n: return b.lift(),b1.lift()
        if b1 == -1 |mod| n: return 'try another a'
        b = b1
    return 'did not work'
