'''
>>> I = DESint(int('011100100110',2))
>>> K = Key(int('0b011001010',2),9)
>>> O = I.enc(K,4)
>>> O
010110001100
>>> O.dec(K,4)
011100100110
>>> I
011100100110
>>> encryptedsecret = DES12('thisisasecret',K)
>>> encryptedsecret
'010111111011101101101100110000000000011010011010110000000000011010011010000101011111011010011010001101110100011111111000110001110011001101110100010111111011'
>>> DES12_d(encryptedsecret,K)
'thisisasecret'

'''
# This is the Sbox, determined by many factors but is the core of making
# the DES algorithm hard to crack.  The order of the 3 bit words appear seems
# arbitrary, but they are in fact carefully chosen.
#          000    001    010    011    100    101    110    111
Sbox = [[['101', '010', '001', '110', '011', '100', '111', '000'],
         ['001', '100', '110', '010', '000', '111', '101', '011']],
        
        [['100', '000', '110', '101', '111', '001', '011', '010'],
         ['101', '011', '000', '111', '110', '010', '001', '100']]]

class DESint(int):
      def __new__(cls, integer,length=12):
            return int.__new__(cls,int(integer))
      
      def __init__(self,integer,length=12):
            self._len = length
            self.leadingzeros = self._len - len(bin(integer)) + 2
            self.string = bin(integer)
            #               000    001    010    011    100    101    110    111
            self.Sbox = [[['101', '010', '001', '110', '011', '100', '111', '000'],
                          ['001', '100', '110', '010', '000', '111', '101', '011']],
                         [['100', '000', '110', '101', '111', '001', '011', '010'],
                          ['101', '011', '000', '111', '110', '010', '001', '100']]]

# The first methods are there to make DES integers print out nicely
# with all necessary leading zeros.
      def __repr__(self):
            return '0'*self.leadingzeros + bin(self)[2:]

      __str__ = __repr__
      
      def __len__(self):
            return self._len

# Then there are come untility methods
      def cat(self,other):
            other = DESint(other,self._len)
            return DESint( (self<< len(other)) + other , 2*self._len )

      def L(self):
            return DESint( self >> (self._len / 2) , self._len / 2 )

      def R(self):
            return DESint( self % (2**(self._len / 2 )) , self._len /2 )
      
      # The next three methods make up the core of the simplified DES algorithm.
      # As long as the number of input and output bits match those of these routines,
      # these methods could change and you'd still have an encryption scheme. Whether or
      # not it would be harder or easier to break is the trick.
      def E(self):
# The expander: length of self should be 6, E returns a 8 bit word
            if self._len != 6: raise ValueError("Only expands 6 bits to 8 bits")
            x = self
            return DESint ( (x&3)+((x&8)>>1)+((x&12)<<1)+((x&4)<<3)+((x&48)<<2) , 8 )

      def S(self):
# Maps 8 bits to 6 bits via the Sbox
            L = self.L()
            R = self.R()
            return DESint( int( Sbox[0][L>>3][L&7],2) , 3 ).cat( DESint( int( Sbox[1][R>>3][R&7],2) , 3 ) )
            
      def f(self,key):
            '''This function maps 6 bits words to 6 bits words and
is the core of the DES algorithm
First, the word is expanded to 8 bits via E,
then XORed with a 8 bit word derived from the key
finally reduced to 6 bits via the Sbox'''
            length = self.E()._len           
            X = DESint( self.E() ^ key , length)
            return X.S()
      
      def round(self,R,K,step):
# performs one round of the simplified DES algorithm with the key starting at the stepth place.
            L = self
            return R, DESint(L^(R.f(K.keys[step])),6)

      # In the following note: differing from the book, a final switch of R and L is incorporated into the
      # encryption algorithm.  This makes the decryption algorithm identical to encryption except for the
      # order of the keys.
      def enc(self,K,rounds=4,decrypt=False):
            R = self.R()
            L = self.L()
            for i in range(rounds):
                  L,R = L.round(R,K,i)
            return R.cat(L)

      def dec(self,K,rounds=4):
            R = self.R()
            L = self.L()
            for i in range(rounds-1,-1,-1):
                  L,R = L.round(R,K,i)
            return R.cat(L)

class Key(DESint):
      def __init__(self,integer,length=9,roundlength=8):
            DESint.__init__(self,integer,length)
            self.keys = []
            D = integer + ((integer<<length))
            step = 0
            while step < length:
                  i = 2*length - step
                  key = (D - ( (D>>i)<<i ))>>(i-roundlength)
                  type(key)
                  self.keys += [ DESint(key,roundlength) ]
                  step += 1
            return


def DES12(input,K,rounds=4):
      # Encrypts any character string by converting each character in the string to a 12 bit DESint
      out = ''
      for char in input:
            out += str(DESint(ord(char)).enc(K,rounds) )
      return out

def DES12_d(output,K,rounds=4):
      # Decrypts a string of bits, 12 bits at a time
      decrypted = ''
      nbits = len(output)
      for n in range(0,nbits,12):
            I = DESint(int(output[n:n+12],2))
            decrypted += chr( I.dec(K,rounds) )
      return decrypted

def intSbox():
      return [ [ [ int(i,2) for i in j] for j in x ] for x in Sbox ]

def niceSbox():
      return [ [ [ DESint( int(i,2), 3 ) for i in j] for j in x ] for x in Sbox ]




		
		
