from matmod import *
from cypari.gen import *
from math import exp
from random import randint, sample

import time

class Timer():
   def __enter__(self): self.start = time.time()
   def __exit__(self, *args): print time.time() - self.start

def log_bf(alpha,beta):
    '''
    Computes log base alpha of beta with modulus N
    by computing every possibility.
    '''
    p = alpha.mod()
    with Timer():
       for k in range(p):
           #print alpha**k
           if alpha**k == beta: return k
       return 'no log'

def log(alpha,beta):
    '''
    uses a BabyStep-GiantStep approach to find the
    discrete log base alpha of beta with modulus p
    alpha is primitive root mod p, a prime number
    beta is mod p. Search for x = k+jN so alpha**x = beta.
    '''
    p = alpha.mod()
    N = (pari(p).sqrt().truncate() + 1)
    with Timer():
       tests = { alpha**k : k for k in xrange(N)}
       # print tests
       y = beta
       a = alpha**(-N)
    with Timer():
       for jN in xrange(0,N**2,N):
           # print 'jN =', jN, y
           if y in tests:
              # print 'k = ', tests[y], 'jN =', jN
              return (jN+tests[y])|mod| (p-1)
           y = y*a
       return 'no log found for ',beta

def prob_match_approx(r,N):
    return (1.-exp(-r**2/(2*float(N))))

def prob_match(r,N):
    p = 1.
    for i in range(1,r):
        p = p*(N-i)/N
    return 1 - p

def log_bday(alpha,beta,r):
    '''
    Uses a birthday attack, probablistic methd to find
    the discrete log base alpha of beta with modulus p
    alpha is primitive root mod p, a prime number
    beta is mod p. r is size of the sample.
    '''
    p = alpha.mod()
    tests = {}
    with Timer():
        J = set(sample(xrange(p),r))
    with Timer():
        K = set(sample(xrange(p),r))
    with Timer():
       tests = { (alpha**k):k for k in K }
    count = 1
    for j in J:
        y = (beta*alpha**(-j))
        if y in tests: return (tests[y]+j)|mod|(p-1)
        count += 1
        if count % 10000 == 0: print count
    return count, False

def log_bday2(alpha,beta,r):
    '''
    Like birthday attack, probablistic methd to find
    the discrete log base alpha of beta with modulus p
    one set is generated from a range of possible exponents -- this
    makes it faster to generate the stored set and, we think, does not
    affect the randomness criteria.
    alpha is primitive root mod p, a prime number
    beta is mod p
    '''
    p = alpha.mod()
    tests = {}
    with Timer():
        J = set(sample(xrange(p),r))
    with Timer():
        tests = { (alpha**k):k for k in xrange(r) }
    count = 1
    for j in J:
        y = (beta*alpha**(-j))
        if y in tests: return count, (tests[y]+j)|mod|(p-1)
        count += 1
        if count % 10000 == 0: print count
    return False




