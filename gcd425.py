
def gcd425(A,B):
    a,b = A,B
    if b == 0:
        return a
    while b >> 0:
        a,b = b,a%b
    return a

def xgcd425(A,B):
    '''We will find x,y such that ax+by=gcd(a,b)'''
#    c = gcd425(A,B)
    x,y,a = 1, 0, A #for every tuple a*x+b*y = c
    x1,y1,b = 0, 1, B #we need to keep track of the previous two equations
    while b >> 0:
        q,r = divmod(a,b)
        x0, y0, c = x,  y, a
        x,  y, a =   x1, y1, b
        x1, y1, b = x0-q*x1, y0-q*y1, c-q*b 
        print x,y,a, 'and', x1,y1,b
    return x,y,a
       
    
