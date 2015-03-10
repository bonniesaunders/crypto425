from matmod import *

def ciphertable(m):
    """
    prints out a ciphertable for multiplication by m
    """
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print ' '.join( [('{:2}'.format(n)) for n in range(26)] )
    print ' '.join( [('{:2}'.format(m*n % 26)) for n in range(26)] )

def multitable(N):
    """
    prints out entire multiplication table mod N
    """
    for m in range(1,N):
        print '{:3}:'.format(m),
        for n in range(1,N):
            print '{:2}'.format(m*n % N),
        print

def powerrow(n,M):
    X = [x |mod| M for x in range(M)]
    row = [[x^n for x in X]] |mod|M 
    print '%2s :'%n, row

def powertable(M,N):
    X = [x |mod| M for x in range(1,M)]
    powers = [ [[x^n for x in X]]|mod|M for n in range(N) ]
    for n in range(N): print '%2s :'%n, powers[n]


def rel_prime(M):
    X = [x |mod| M for x in range(M)]
    m = Matmod(M).gen.phi()
    N = []
    powers = []
    for n in range(m):
        if gcd_bss(n,m)==1:
            N = N + [n]
            powers = powers + [ [[x^n for x in X]] |mod| M ]
    for n in N: print '%2s :'%n, powers[N.index(n)]
    
def gcd_bss(a,b):
    if b == 0:
        return a
    while b >> 0:
        a,b = b,a%b
    return a
