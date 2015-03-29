# -*- coding: utf-8 -*-
'''
>>> key = State(0b0011001100001111)
>>> rkeys = round_keys(wbytes(key))
>>> S = State(0b0101011011001001)
>>> S0 = S.ARK(rkeys[0])
>>> S1 = S0.NybbleSub()
>>> S2 = S1.ShiftRow()
>>> S3 = S2.MixColumn()
>>> S4 = S3.ARK(rkeys[1])
>>> S5 = S4.NybbleSub()
>>> S6 = S5.ShiftRow()
>>> S7 = S6.ARK(rkeys[2])
>>> S
0101 0110 1100 1001
>>> S0
0110 0101 1100 0110
>>> S1
1000 0001 1100 1000
>>> S2
1000 1000 1100 0001
>>> S3
1110 1110 1000 0100
>>> S4
0010 0100 0100 0001
>>> S5
1010 1101 1101 0100
>>> S6
1010 0100 1101 1101
>>> S7
0100 0010 1111 1110
'''
class Poly:   
    def __init__(self,integer,mod = 2):
        self.degree = len(bin(integer)[2:])-1
        if integer == 0: self.degree = -1
        self.mod = mod
        self.bin = bin(integer)[2:]
        self.int = int(integer)
        self.hex = hex(integer)[2:]
        self.oct = oct(integer)[1:]
        self.vector = [ int(char) for char in self.bin ]
        

    def __repr__(self):
        if self.int == 0: return '0'
        s = self.bin
        n = len(s)
        p = [ n-i-1 for i in range(n) if int(s[i]) ]
        m = [ 'x^{}'.format(i) for i in p if not (i==1 or i==0) ]
        if 1 in p: m.append('x')
        if 0 in p: m.append('1')
        return ' + '.join(m)
    
    def __add__(self, other):
        if other is 1: other = Poly(1)
        return Poly(self.int ^ other.int)

    def __sub__(self,other):
        return self + other

    def __lshift__(self,other):
        return Poly(self.int << other)

    def __rshift__(self,other):
        return Poly(self.int >> other)

    def __getitem__(self,index):
        return ( self.int >> index) & 1

    def __eq__(self,other):
        if isinstance(other,int): return self.int == other
        return self.int == other.int

    def __hash__(self):
        return self.int

    def __pow__(self,other):
        #other must be integer
        result = Poly(1)
        for i in xrange(other): result *= self
        return result

    def __mod__(self,mod):
        n = mod.degree
        y = self
        m = y.degree
        while m >= n:
            if m >= n: y = y + (mod << (m-n))
            m = y.degree
        return y

    def __mul__(self,other):
        n = self.degree + 1
        s = Poly(0)
        if other == 1: return self
        if other == 0: return s
        for i in range(n):
            if self[i]: s += (other << i)
        return s

    def __call__(self,x):
        return eval(str(self).replace('^','**'))%self.mod

    def __div__(self,other):
        return self.divmod(other)[0]

    def GFrep(self,n):
        return '0'*(n-self.degree-1) + self.bin

    def inverse(self,mod):
        g,n,m = self.xgcd(mod)
        if g == 1: return n
        return 'no inverse'

    def divmod(self,mod):
        n = mod.degree
        y = self
        m = y.degree
        d = Poly(0)
        while m >= n:
            y = y + (mod << (m-n))
            d += Poly(2**(m-n))
            m = y.degree
        return d,y

    def GFmult(self,other,mod=None):
        if not isinstance(mod,Poly): return self*other
        n = self.degree+1
        s = Poly(0)
        for i in range(n):
            if self[i]: s = ( s + (other<<i) ) % mod
        return s

    def RotNyb(self):
        X4 = Poly(0b10000)
        return self.divmod(X4)[0]+self.divmod(X4)[1]*X4

    def SubNyb(self):
        # 
        X4 = Poly(0b10000)
        n1 = self.divmod(X4)[0]
        n0 = self.divmod(X4)[1]
        return Sbox()[n1.int]*X4+Sbox()[n0.int]

    def xgcd(self,B):
        A = self
        a, b = A, B
        n1, m1, n, m = Poly(0), Poly(1), Poly(1), Poly(0)
        if B is 0:  return A, Poly(1), Poly(0)
        r = b
        d = r.degree
        while d >= 0:
            g = r
            q,r = a.divmod(b)
            n1,m1,n,m = n-q*n1,m-q*m1,n1,m1
            a, b = b, r
            d = r.degree
            #A*n1+B*m1=r, last time will be r = 0, so A*n+B*m=g 
        return g,n,m

class State(Poly):
    
    def __init__(self,integer,mod = 2,bits=16):
        if isinstance(integer,Poly): integer = integer.int
        self.bits = bits
        Poly.__init__(self,integer,mod)
        self.bin = '0'*(bits - len(self.bin)) + self.bin
        q,r=divmod(bits,4)
        self.q = q
        self.r = r
        self.poly = Poly(integer)
        self.nybs2 = [ Poly(int(self.bin[4*i:4*(i+1)],2))  for i in range(q) ]
 
    def __repr__(self):
        if self.bits == 6: return self.bin
        return ' '.join( [ self.bin[4*i:4*(i+1)] for i in range(4) ] )

    def nybs(self):
        q = self.q
        return [ Nybble(int(self.bin[4*i:4*(i+1)],2))  for i in range(q) ]

    def ShiftRow(self):
        #linear mixing of rows
        X4 = Poly(0b10000)
        return State(self.nybs()[0]*(X4**3)+self.nybs()[3]*(X4**2)+self.nybs()[2]*X4+self.nybs()[1])

    def ARK(self,key):
        # XOR with round key
        return State(self + key)

    def MixColumn(self,pmod=Poly(0b10011)):
        #linear mixing columns
        X2 = Poly(0b100)
        b = self.nybs()
        return nybs_to_state([ b[0]+b[1].GFmult(X2,pmod), b[0].GFmult(X2,pmod)+b[1], 
                               b[2]+b[3].GFmult(X2,pmod), b[2].GFmult(X2,pmod)+b[3] ])

    def MixColumnInv(self,pmod=Poly(0b10011)):
        A = Poly(0b1001)
        B = Poly(0b10)
        b = self.nybs()
        return nybs_to_state([ ( b[0]*A+b[1]*B) % pmod, (b[1]*A+b[0]*B) % pmod, 
                               ( b[2]*A+b[3]*B) % pmod, ( b[3]*A+b[2]*B) % pmod ])

    def NybbleSub(self):
        # ByteSub in full AES: non-linear layer for resistance to differential and linear attacks.
        return nybs_to_state( [ Sbox()[nybble.int] for nybble in self.nybs() ] )

    def NybbleSubInv(self):
        return nybs_to_state( [ Poly(Sbox().index(nybble)) for nybble in self.nybs() ] )

    def Musa_encrypt(self,key):
        # Encrypts 16-bit State using a 16-bit key 
        rkeys = round_keys(wbytes(key))
        return self.ARK(rkeys[0]).NybbleSub().ShiftRow().MixColumn().ARK(rkeys[1]).NybbleSub().ShiftRow().ARK(rkeys[2])
    
    def Musa_decrypt(self,key):
        # Decrypts 16-bit State using a 16-bit key 
        rkeys = round_keys(wbytes(key))
        return self.ARK(rkeys[2]).ShiftRow().NybbleSubInv().ARK(rkeys[1]).MixColumnInv().ShiftRow().NybbleSubInv().ARK(rkeys[0])


class Round(State):

    def __init__(self,integer,mod = 2):
        State.__init__(self,integer,mod,12)
        L,R = self.divmod(Poly(64))
        self.L,self.R = State(L,2,6),State(R,2,6)
        
    def __repr__(self):
        return ' '.join( [ self.bin[6*i:6*(i+1)] for i in range(2) ] )

    def switch(self):
        return Round(self.R.int*64+self.L.int)

    def f(self,K):
        X = R.expander + K

    def expander(self):
        string = self.L.bin
        return self

class Nybble(State):

    def __init__(self,integer,mod = 2):
        if isinstance(integer,Poly): integer = (integer.int % 16)
        State.__init__(self,integer,mod,4)
        self.Sbox = [[['101', '010', '001', '110', '011', '100', '111', '000'],
          ['001', '100', '110', '010', '000', '111', '101', '011']],
         [['100', '000', '110', '101', '111', '001', '011', '010'],
          ['101', '011', '000', '111', '110', '010', '001', '100']]]

    def S(self,i=1):
        S = self.Sbox
        row,col = self.divmod(Poly(8))
        return S[i-1][row.int][col.int]

   
def rijndael_poly():
    return Poly(0b100011011)

def Sbox(pmod = Poly(0b10011), a = Poly(0b1101),b = Poly(0b1001),qmod = Poly(0b10001)):
    sbox = []
    for n in xrange(16):
        if n == 0: np = Poly(0)
        else: np = Poly(n).inverse(pmod)
        sbox.append(((a*np+b) % qmod) )
    return sbox

def RCON(i,pmod=Poly(0b10011)):
    X = Poly(2)
    return (X**(i+2) % pmod ) * (X**4)

def wbytes(key):
    X8 = Poly(0b100000000)
    w = list(key.divmod(X8))
    for i in range(2):
        w.append(w[2*i] + RCON(i+1) + w[2*i+1].RotNyb().SubNyb())
        w.append(w[2*i+1]+w[2*i+2])
    return w

def round_keys(w):
    # Returns 3 rounds of 8-bit roundkeys from the given 12-bit key
    X8 = Poly(0b100000000)
    return [ State(w[2*i]*X8 + w[2*i+1]) for i in range(3) ]

def ARK(state,key):
    return state + key

def nybs(state,bits=4,power=3):
    X = Poly(2**bits)
    Y = X**power
    b = [0 for n in range(bits)]
    r = state
    for i in range(power):
        b[i],r = r.divmod(Y)
        Y =  Y / X
    b[power]=r
    return b

def nybs_to_state(nybs):
    X4 = Poly(0b10000)
    return State(nybs[0]*(X4**3)+nybs[1]*(X4**2)+nybs[2]*X4+nybs[3])

def genGF2(gen,mod):
    n = mod.degree
    y = gen
    i = 1
    while not (y == 1):
        print '{0:4}: {1:4} {1:0{2}b}'.format(i,y.int,n),y
        y = y.GFmult(gen,mod)
        i+=1
    print '{0:4}: {1:4} {1:0{2}b}'.format(i,y.int,n),y       

def multitable(polymod):
    """
    prints out entire polynomial multiplication by poly mod table
    elements are represented as Z/N
    """
    n = polymod.degree
    N = 2**n 
    for m in range(1,N):
        print '{:3}:'.format(m),
        print ' '.join( [ '{:3}'.format(Poly(m).GFmult(Poly(n),polymod).int) for n in range(1,N) ] )

def multitablebin(polymod):
    """
    prints out entire polynomial multiplication by poly mod table
    elements are represented as Z/N
    """
    n = polymod.degree
    N = 2**n
    for m in range(1,N):
        print '{}:'.format(Poly(m).GFrep(n)),
        print ' '.join( [ '{}'.format(Poly(m).GFmult(Poly(k),polymod).GFrep(n)) for k in range(1,N) ] )

def multitablehex(polymod):
    """
    prints out entire polynomial multiplication by poly mod table
    elements are represented in hex Z/N
    """
    n = polymod.degree
    N = 2**n 
    for m in range(1,N):
        print '{:02x}:'.format(m),
        print ' '.join( [ '{:02x}'.format(Poly(m).GFmult(Poly(n),polymod).int) for n in range(1,N) ] )

def powtable(polymod):
    """
    prints out entire polynomial power table
    elements are represented as Z/N
    """
    n = polymod.degree
    N = 2**n 
    for m in range(1,N):
        print '{:3}:'.format(m),
        print ' '.join( [ '{:3}'.format(((Poly(n)**m) % polymod ).int ) for n in range(1,N) ] )


