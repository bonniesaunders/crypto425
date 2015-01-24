from matmod import *

Lbin = 0b11001010001001000000111101001100011010111011011111100001011001110010100010010000001111010011000110101110110

L101=[1,0,1,0,0,1,1,0,1,1,0,0,0,1,0,0,1,0,0,0,0,
      1,1,1,0,0,0,0,0,1,0,1,1,1,1,1,1,0,0,1,0,1,
      0,1,0,0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,0,1,
      1,0,1,0,0,1,1,0,1,1,0,0,0,1,0,0,1,0,0,0,0,
      1,1,1,0,0,0]
L100=[1,0,0,1,1,0,0,1,0,0,1,1,1,0,0,0,1,1,0,0,0,
      1,0,1,0,0,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,0,
      1,0,1,0,1,0,0,1,0,1,1,0,1,1,0,1,0,1,1,0,0,
      0,0,1,1,0,1,1,1,0,0,1,0,1,0,1,1,1,1,0,0,0,0
      ,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0]
L011=[0,1,1,0,0,0,1,0,1,0,1,1,1,0,0,1,1,1,0,1,0,
      1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,1,0,1,1,1,0,
      0,1,1,1,0,1,0,1]

class BIN():
    def __init__(self,L):
        """ If L is a list or a string of 1's and 0's or if L is an int or logn integer,
BIN has all attributes: list, string, Matmod integer, Matmod vector, and
Matmod row and column matrices, all mod 2.
"""
        self.L = L
        if isinstance(L,list):
            self.l = L
            self.s = ''.join([ str(x) for x in L])
            self.N = Matmod( int(self.s,2), None )
        if isinstance(L,int) or isinstance(L,long):
            self.N = Matmod( L, None )
            self.s = bin(L)[2:]
            self.l = [ int(x) for x in self.s ]
        if isinstance(L,str):
            self.s = L
            self.N = Matmod( int(L,2), None )
            self.l = [ int(x) for x in L ]
        self.v = Matmod( self.l, 2 )     #the Matmod vector
        self.rmat = Matmod( [ self.v ] ) #the row matrix
        self.cmat = self.rmat.transpose()#the column matrix
            
    def __repr__(self):
        return self.s

##class LFSR():
##    """In progress; not clear what this is about about it clearly wants to generate a sequence.
##"""
##    def __init__(self,ivector,cvector):
##        self.initial = ivector
##        self.cvector = cvector
##        self.lfsr = BIN(self.generate(self,self.)
##       
##    def bit_sum(self,x):
##        L = len(bin(x))-2
##        return sum([( x & (1<<j)) >> j for j in range(L) ]) % 2
##
##    def nextbit(self,x):       
##        return self.bit_sum(x & self.generator)
##
##    def vec(self,x):
###        print bin(x)
##        return ( (x << 1) + self.nextbit(x) )
##
##    def generate(self,x,n):
##        if n == 0:
##            return self.vec(x)
##        else:
##            return self.generate(self.vec(x),n-1)

      
def LFSR_gen(GM,initial,length):
    """
    GM is the generating matrix
    intitial is Mod 2 1xn column matrix
    """
    L = []
    V = BIN(initial).cmat
    size = V.shape()[0]
    D = GM^(size)
    for i in range(length/size):
        L = L + [ V.lol[i][0] for i in range(size) ]
        V = D*V
    return BIN(L)

def make_GM(c):
    """ c is a string or list of the coefficients(only 1's 0's allowed that for ther rcurrence relation
c_0*x_m + . . . c_n*x_m+n = x_m+n+1.
"""
    c = [ int(x) for x in c ]
    N = len(c)
    I = identity(N-1)
    z = Matmod( [ [0 for x in range(N-1)] ],2)
    M = Matmod( [z,I] ).transpose()
    C = Matmod ( [ c ] , 2 )
    return Matmod( [M, C] )
     

def make_M(data,n,start=0):
    return [ data[m:m+n] for m in range(start,start+n) ] |mod| 2

def det_seq(data,length=25):
    "data is a list of integers 1's or 0's"
    string = ''
    for n in range(1,length):
        M = make_M(data,n)
        if (M.det().lift() == 1):
            finalM = M
#            print M
        string += '{:2}'.format(M.det().lift(),)
    return string,finalM

##def list_number(L):
##    N = len(L)
##    return sum([ L[-x-1]<<x for x in range(N) ])
