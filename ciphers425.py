from matmod import *
from messages import *

class Cipher:

  def encrypt(self, plaintext):
      """
      Return encrypted version of text.
      """
      # Subclasses override this.
      ciphertext=''
      return ciphertext

  def decrypt(self, ciphertext):
      """
      Return decrypted version of text.
      """
      plaintext=''
      # Subclasses override this.
      return plaintext

  def crack(self, ciphertext):
      """
      Return decrypted version of textand the key.
      """
      plaintext=''
      key = ''
      # Subclasses override this.
      return key, plaintext

  
class AffineCipher(Cipher):

    def __init__(self, m = 1, b = 0):
        self.m, self.b = m , b
        if not ( isinstance(m, int) and isinstance(b, int) ):
            raise ValueError("m and b must be integers.")
              
    def change_key(self,m,b):
        if not ( isinstance(m, int) and isinstance(b, int) ):
            raise ValueError("m and b must be integers.")
        self.m, self.b = m , b
        return m,b
      
    def check_key(self,alphabet,m = None):
      if m == None: m = self.m
      if xgcd(m,len(alphabet))[0] != 1:
        return ( "m is not relatively prime to the length of the alphabet. "
        "m is not a good multiplicative key. "
        "You can encrypt but decryption is not reliable." )
      else:
        return ( "m is relatively prime to the length of the alphabet. "
        "m is a good multiplicative key." )

    def ciphertable(self, alphabet):
        cipheralphabet = self.encrypt(Message(alphabet,alphabet))
        print ''.join( ['{:2}'.format(x) for x in alphabet])
        print ''.join( ['{:2}'.format(x) for x in cipheralphabet])


    def affine(self, message, m , b):
        """
        transforms text by multiplying by m and then adding b
        """
        alphabet = message.alphabet
        mod = message.mod
        textlist=[alphabet[(m*alphabet.index(c)+b)% mod]
                  if c in alphabet else c
                  for c in message]
        return Message(''.join(textlist),alphabet)   
           
    def encrypt(self,message):
        """
        Encrypts by affine cipher, key x(m,b)
        """
        if not isinstance(message,Message): return 'bad Message'
        return self.affine(message,self.m,self.b)

    def decrypt(self,message = None):
        """
        Decrypts ciphertext that was encrypted with affine cipher, key (m,b)
        """
        if not isinstance(message,Message): raise ValueError('bad Message')
        gcd,minv,n = xgcd(self.m,message.mod)
        if gcd != 1: raise ValueError('m is not relatively prime to mod')
        return self.affine(message,minv,-minv*self.b)
          
class Caesar(AffineCipher):
    """
    Uses AffineCipher with m = 1.
    """
    def __init__(self, b=0):
        AffineCipher.__init__(self,1,b)

    def change_key(self,b):
        self.b = b
        return

    def crack1(self,message):
        """
        Prints out possible keys and decryptions of message with that key
        """
        alphabet = message.alphabet
        mod = message.mod
        for j in range(mod):
            newtext=''
            for i in range(len(message)):
                newtext += alphabet[(alphabet.index(message[i])-j)%mod]
            print 'key = {:2}: '.format(j), newtext

class SubstitutionCipher(Cipher):

    def __init__(self, alphabet, cipheralphabet):
        self.cipheralphabet = cipheralphabet
        self.alphabet = alphabet
        if len(alphabet) != len(cipheralphabet):
          raise ValueError('alphabets do not have same length')
 
    def encrypt(self,text):
        """
        returns encryted message with alphabet equal to cipher cipheralphabet
        """
        alphabet = self.alphabet
        cipheralphabet = self.cipheralphabet
        return Message(text,alphabet).substitute(cipheralphabet)

    def decrypt(self,message):
        """
        Decrypts ciphertext that was encrypted with affine cipher, key (m,b)
        """
        return message.substitute(self.alphabet)


class Vigenere(Cipher):
  
    def __init__(self,keyword = 'KEYWORD'):
      self.keyword = keyword.upper()
      self.keylength = len(self.keyword)

    def change_keyword(self,keyword):
      self.keyword = keyword.upper()
      self.keylength = len(self.keyword)
      return keyword
    
    def vig(self,message):
      alphabet = message.alphabet
      key = self.keyword
      kl = self.keylength
      L = len(message)
      textlist = list(message)
      count = 0
      newtext = ''
      while len(textlist):
        char = textlist.pop(0)     
        if char in alphabet:
          B = alphabet.index(key[count%kl])
          newtext += alphabet[(alphabet.index(char) + B) % message.mod]
          count+= 1
        else:
          newtext += char
      return Message(newtext,alphabet)

    def encrypt(self,message):
      if not isinstance(message,Message): return 'bad Message'
      return self.vig(message)

    def decrypt(self,message):
      """
decrypting will change the keyword to the decrypting keyword
use inverse_keyword to revert back and encrypt again
"""
      if not isinstance(message,Message): return 'bad Message'
      alphabet = message.alphabet
      mod = message.mod
      newkeyword = ''.join([alphabet[((mod - alphabet.index(letter)) % mod)]
                          for letter in self.keyword])
      self.change_keyword(newkeyword)
      return self.vig(message)
    
                                            
class HillCipher(Cipher):
  
    def __init__(self, matrix=Matmod([[1,2],[2,1]],26)):
        self.matrix = matrix
        self.dim = matrix.shape()[0]
     
    def blocks(self,message):
        alphabet = message.alphabet
        dim = self.dim
        ciphernumbers = message.to_integers()
        return [ [ciphernumbers[i] for i in range(dim*j,dim*(j+1))]
              for j in range(len(ciphernumbers)//dim)] |mod| message.mod

    def encrypt(self,message):
        alphabet = message.alphabet
        D = self.blocks(message) * self.matrix
        nrows,columns = D.shape()
#        print nrows,columns,D
        return Message(''.join( [ ''.join( [ alphabet[x.lift()] for x in D[j] ] )
                          for j in range(nrows) ] ),alphabet) 

    def decrypt(self,message):
        """
        Created by Nathan Lavy. Spring 2013.
        This decrypts the given string.  The string must be of length divisible by the dimension of the matrix.
        If the string is not divisible by the dimension of the matrix, then the extra characters will be truncated.
        """
        
        ## This cannot work for strings of length not divisible by the dimension of the matrix.
        ## This is because all of the characters in then encrypted string
        ##    provide information that is used to decrypt the string.
        ## example:
        ##    Suppose we have: m = [ 00, 00, 01 ]
        ##                         [ 00, 01, 00 ]
        ##                         [ 01, 00, 00 ]  mod 26
        ##    Suppose further that there is only one character that is unknown.
        ##    The plaintext would look like: '?xx', where '?' can be any letter (the pad is 'x', which integer value is 23)
        ##    The encrypted string would look like: [ 23, 23, $ ], where $ is the encrypted number for ?
        ##    The equations that generated this is:
        ##        ? * 0 + 23 * 0 + 23 * 1 = 23 mod 26
        ##        ? * 0 + 23 * 1 + 23 * 0 = 23 mod 26
        ##        ? * 1 + 23 * 0 + 23 * 0 =  $ mod 26
        ##    If the encrypted string is truncated, then the encrypted string would be: [ 23 ]
        ##    If we would try to decrpyt this with a system of equations, they would look like:
        ##        a * 0 + 23 * 0 + 23 * 1 = 23 mod 26  --->   23 = 23 mod 26
        ##        a * 0 + 23 * 1 + 23 * 0 =  b mod 26  --->    b = 23 mod 26
        ##        a * 1 + 23 * 0 + 23 * 0 =  c mod 26  --->    a =  c mod 26
        ##    From this, a and c can be anything (as long as they are equivalent mod 26), which means we cannot decrypt it.
        ##    Because I was able to find a situation that needed all of the characters (numbers) in the encrypted
        ##        string (made with the pad) to be able to decrypt, the pad must be kept in the encrypted string.

        alphabet = message.alphabet
        matrix_inverse = self.matrix ^ -1
        D = self.blocks(message) * matrix_inverse
        nrows,columns = D.shape()
        return Message(''.join( [ ''.join( [ alphabet[x.lift()] for x in D[j] ] )
                          for j in range(nrows) ] ),alphabet)

    def unblock(self,D,alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        nrows,columns = D.shape()
        return Message(''.join( [ ''.join( [ alphabet[x.lift()] for x in D[j] ] )
                          for j in range(nrows) ] ),alphabet)
        

class RSA(Cipher):
    ''' N is the product of two large primes which are not known for encrypting,
but must be known to decrypt.  e is a number relative prime to (p-1)*(q-1)
    '''
    def __init__(self,N,e,p=1,q=1):
       self.N, self.p, self.q, self.e = N,p,q,e
       if p!= 1:
         self.N = p*q

    def encrypt(self,message):
        ''' message is an integer.
        '''
        m = Matmod(message,self.N)
        return (m^self.e).lift()

    def decrypt(self,message):
        ''' message is an integer.
        '''
        dmod = (self.p-1)*(self.q-1)
        if dmod == 0:
          return 'can\'t decrypt'
        else:
          m = Matmod(message,self.N)
          d = (Matmod(self.e,dmod))^-1
          return (m^(d.lift())).lift()
        
 
def cards():
    alphabet = 'A234567890JQK'
    return Message('JA' + 'C'.join(alphabet) + 'C' +
                   'D'.join(alphabet) + 'D' + 'H'.join(alphabet) + 'H' +
                   'S'.join(alphabet) +'S' + 'JB', alphabet = 'A234567890JQK')

def xgcd(A,B):
    """
    Finds g=gcd(A,B) and solves the equation A*n+B*m=gcd(A,B)
    """
    a, b = A, B
    n1, m1, n, m = 0, 1, 1, 0
    if B == 0:
      return A, 1, 0
    r = b
    while r > 0:
        g = r
        q,r = divmod(a,b)
        n1,m1,n,m = n-q*n1,m-q*m1,n1,m1
        a, b = b, r       
        #A*n1+B*m1=r, last time will be r = 0, so A*n+B*m=g 
    return g,n,m


      

     

#if __name__ == '__main__':
    
