from matmod import *
from cypari.gen import *
from math import exp
from random import randint, sample

import time

class Timer():
   def __enter__(self): self.start = time.time()
   def __exit__(self, *args): print time.time() - self.start

def log_bf(alpha,beta,N):
    '''
Computes log base alpha of beta with modulus N
by computing every possibility.
'''
    with Timer():
       for k in range(N):
           if alpha**k == beta: return k
       return 'no log'

def log_bf2(alpha,beta,N):
    '''
    Brute Force method computes the discrete log base alpha of beta with modulus N
    by checking every possible alpha**x. Computes alpha**x slower than log_bf.

'''
    with Timer():
       y = 1 |mod| beta.mod()
       for x in xrange(N):
           if y == beta: return x, y
           y = y*alpha
       return 'no log less than {}'.format(N)

def log(alpha,beta,p):
    '''
    uses a BabyStep-GiantStep approach to find the
    discrete log base alpha of beta with modulus p
    alpha is primitive root mod p, a prime number
    beta is mod p
    '''
    N = (p.sqrt().truncate() + 1)
    tests = {}
    y = 1 |mod| p
    print 'N = ', N
    with Timer():
       for k in xrange(N):
            tests[y] = k
            y = y*alpha
       y = beta
       a = alpha**(-N)
       count = 1
       for l in xrange(0,N**2,N):
           if y in tests:
              return count, (l+tests[y])|mod| (p-1)
           y = y*a
           count += 1
       return 'no log found for ',beta

def log2(alpha,beta,p):
    '''
    uses a BabyStep-GiantStep approach to find the
    discrete log base alpha of beta with modulus p
    alpha is primitive root mod p, a prime number
    beta is mod p
    '''
    N = (p.sqrt().truncate() + 1)
    with Timer():
       tests = { alpha**k : k for k in xrange(N)}
       y = beta
       a = alpha**(-N)
       count = 1
       for l in xrange(0,N**2,N):
           if y in tests:
              return count, (l+tests[y])|mod| (p-1)
           y = y*a
           count += 1
       return 'no log found for ',beta

def prob_match_approx(r,N):
    return (1.-exp(-r**2/(2*float(N))))

def prob_match(r,N):
    p = 1.
    for i in range(1,r):
        p = p*(N-i)/N
    return 1 - p

def log_bday(alpha,beta,p,r):
    '''
    Uses a birthday attack, probablistic methd to find
    the discrete log base alpha of beta with modulus p
    alpha is primitive root mod p, a prime number
    beta is mod p
    '''
    tests = {}
    with Timer():
        L = set(sample(xrange(p),r))
    with Timer():
        K = set(sample(xrange(p),r))
    with Timer():
       tests = { (alpha**k):k for k in K }
    count = 1
    for l in L:
        y = (beta*alpha**(-l))
        if y in tests: return count, (tests[y]+l)|mod|(p-1)
        count += 1
        if count % 10000 == 0: print count
    return count, False

def log_bday2(alpha,beta,p,r):
    '''
    Like birthday attack, probablistic methd to find
    the discrete log base alpha of beta with modulus p
    one set is generated from a range of possible exponents -- this
    makes it faster to generate the stored set and, we think, does not
    affect the randomness criteria.
    alpha is primitive root mod p, a prime number
    beta is mod p
    '''
    tests = {}
    with Timer():
        L = set(sample(xrange(p),r))
    with Timer():
        tests = { (alpha**k):k for k in xrange(r) }
    count = 1
    for l in L:
        y = (beta*alpha**(-l))
        if y in tests: return count, (tests[y]+l)|mod|(p-1)
        count += 1
        if count % 10000 == 0: print count
    return False




