from matmod import *
from cypari.gen import pari
from random import randint

def MR(n):
    k=1
    if n % 2 == 0: return 'composite: factor is 2'
    m = (n-1) / 2
    while ( m%2 ==0 ):
        k += 1
        m = m / 2
#n-1 = m*2^k
    print 'n-1 = {}*2^{}'.format(m,k)
    a = randint(2,n-1) |mod| n
    print 'a = ', a
    b = a**m
    print 'b_{}={}'.format(0,b)
    if b.lift()==1 or b.lift() == n-1:
        return 'probably prime'
    b1 = b**2
    l = 0
    while l < k:
        print 'b_{}={}'.format(l+1,b1)
        if b1.lift()==1:
            #this means that b is a false square root
            return 'composite: factor is', xgcd(b.lift()-1,n)[0]
        if b1.lift()==(n-1): return 'probably prime'
        b,b1 = b1,b1**2
        l+=1
    if b1.lift() is not (n-1): return 'composite: '
    return 'probably prime'
