from matmodtest import *

def d_log(alpha,beta,p):
    """
alpha and beta are mod p numbers. p is pari integer.
returns solution, x, to alpha**x = beta mod p
    """
    N = (p-1).sqrt().floor() + 1
    list_one = { alpha**j:j for j in xrange(N) }
#    print list_one
#    print 'N={}'.format(N)
    for k in xrange(N):
#        print k,
        x = list_one.get(beta*alpha**(-N*k))
        if x is not None: return x,x+N*k
    return 'no log'
