from matmod import *
from cypari.gen import pari

def chinese(a,b):
    '''
finds x = a mod n and x = b mod m; x is reduced mod nm 
    '''
    return Matmod(gen.chinese(a.gen,b.gen))

def xgcd(a,b):
    '''
returns (g,u,v) so that a*u + b*v = g and g = gcd(a,b).
    '''
    return gen.xgcd(pari(a),pari(b))


def crt_bf(a,b,big,little):
    """
    solves x = amod (big) and x = b mod (little)
    """
    x,y = a,b
    while not (x == y):
       x = x + big
       print x,y
       while ( y < x):
          y = y + little
          print x,y
    return x

def crt(x1,x2,p1,p2):
    """
    solves x = x1modp1 and x = x2modp2
    """
    g,n,m = xgcd(p1,p2,x2-x1)
    return (p1*n + x1) |mod| p1*p2
    
def gcd(a,b):
    if b == 0: return a
    else: return gcd(b,divmod(a,b)[1])
    
def xgcd_diophantine(A,B,C):
    """
    Finds g=gcd(A,B) and solves the equation A*n+B*m=C*gcd(A,B)
    """
    a, b = A, B
    n1, m1, n, m = 0, C, C, 0
    if B == 0:
      return C, 0, A
    r = b
    while r > 0:
        g = r
        r = a % b
        q = (a-r)/b  
        n1,m1,n,m = n-q*n1,m-q*m1,n1,m1
        a, b = b, r       
        #A*n1+B*m1=r, last time will be r = 0, so A*n+B*m=g 
    return g,n,m

