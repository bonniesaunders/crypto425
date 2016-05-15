from matmod import *
from messages import *
eng_freq = [('a', 8.2), ('b', 1.5), ('c', 2.8), ('d', 4.3), ('e', 12.7), ('f', 2.2), ('g', 2), ('h', 6.1), ('i', 7), ('j', 0.2), ('k', 0.8), ('l', 4), ('m', 2.4), ('n', 6.8), ('o', 7.5), ('p', 1.9), ('q', 0.1), ('r', 6), ('s', 6.3), ('t', 9.1), ('u', 2.8), ('v', 1), ('w', 2.4), ('x', 0.2), ('y', 2), ('z', 0.1)]
 
class Cipher:

  def encrypt(self, plaintext):
      """
      Encrypt 'plaintext' and return 'ciphertext'
      """
      if not isinstance(plaintext,Message): return 'Plaintext is not Message instance'
      # Subclasses override this.
      ciphertext = Message('',plaintext.alphabet)
      return ciphertext

  def decrypt(self, ciphertext):
      """
      Decrypt 'ciphertext and return 'plaintext'.
      """
      if not isinstance(ciphertext,Message): return 'Plaintext is not Message instance'
      plaintext=''
      # Subclasses override this.
      return plaintext

  def crack(self, ciphertext):
      """
      Return decrypted version of text and the key.
      """
      if not isinstance(ciphertext,Message): return 'Plaintext is not Message instance'
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

    def ciphertable(self, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        cipheralphabet = self.encrypt(Message(alphabet,alphabet))
        return ''.join( ['{:2}'.format(x) for x in alphabet]),''.join( ['{:2}'.format(x) for x in cipheralphabet])


    def affine(self, message, m , b):
        """
        Apply affine cipher with key multiplicative key m and additive key b
        """
        alphabet = message.alphabet
        modulus = message.modulus
        textlist=[alphabet[(m*alphabet.index(c)+b)% modulus]
                  if c in alphabet else c
                  for c in message]
        return Message(''.join(textlist),alphabet)   
           
    def encrypt(self,message):
        """
        Encrypts by affine cipher, key (m,b)
        """
        if not isinstance(message,Message): return 'bad Message'
        return self.affine(message,self.m,self.b)

    def decrypt(self,message = None):
        """
        Decrypts ciphertext that was encrypted with affine cipher, key (m,b)
        """
        if not isinstance(message,Message): raise ValueError('bad Message')
        gcd,minv,n = xgcd(self.m,message.modulus)
        if gcd != 1: raise ValueError('m is not relatively prime to modulus')
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
        modulus = message.modulus
        list = []
        for j in range(modulus):
            newtext=''
            for i in range(len(message)):
                newtext += alphabet[(alphabet.index(message[i])-j)%modulus]
            list.append( 'key = {:2}: '.format(j) + newtext )
        return list

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
          newtext += alphabet[(alphabet.index(char) + B) % message.modulus]
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
      if not isinstance(message,Message): return 'message must be Message instance'
      alphabet = message.alphabet
      modulus = message.modulus
      newkeyword = ''.join([alphabet[((modulus - alphabet.index(letter)) % modulus)]
                          for letter in self.keyword])
      self.change_keyword(newkeyword)
      return self.vig(message)
  
    def crack(self,message):
        E = message.strip()
#Find the highest correlation of data with shifts of itself (shifts of 1 to 20)
        shifts = 20
        shift_cor = E.shift_test(shifts)[3:]
        keylength = shift_cor.index(max(shift_cor)) + 3
#Group data mod the keylength. Analize frequencies to find likely shift for each group.
#This is a weak spot if a multiple of the keylength is determined then the data per
#group is less and therefore analysis is less accurate.
        groups = E.groups(keylength)
        group_freq = [ Message(groups[i]).frequencies() for i in range(keylength) ]
        keyword = self.find_keyword(E,keylength,groups,group_freq)
        return keyword, self.decrypt(message)
      
    def find_keyword(self,message,keylength,groups,group_freq):
        keyword=Message('')
        for i in range(keylength):
             shift = message.shift_correlation(group_freq[i],eng_freq)
             shift.sort(key = lambda x: x[1], reverse=True)
             keyword += message.alphabet[ -shift[0][0] ]
        factors = []
#Look for repeating pattern in keyword and reduce accordingly        
        for f in range(3,keylength):
             if keylength % f == 0: factors += [f]
        for f in factors:
          sub = keyword[:f]
          if len(sub)*keyword.find_all(sub) == len(keyword):
            keyword = sub
            break
        self.change_keyword(keyword)
        return keyword
                                               
class HillCipher(Cipher):
  
    def __init__(self, matrix=Matmod([[1,2],[2,1]],26)):
        self.matrix = matrix
        self.dim = matrix.shape()[0]
     
    def blocks(self,message):
        alphabet = message.alphabet
        dim = self.dim
        ciphernumbers = message.to_integers()
        return [ [ciphernumbers[i] for i in range(dim*j,dim*(j+1))]
              for j in range(len(ciphernumbers)//dim)] |mod| message.modulus

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
    
