try:
  from matmod import *
except: pass

A = 'YBRWY JFM N QCGYFR GIL SUZJX WJMFJ. NUJ VVL VBDM VS NUJ HRNAUGIEMIBI WBSMGFHGQS GJUFJX UNG. FTGRYCZJM GMYL TZSJLRI BVR U PMIVHY OJNJJYA F HVHERQ UAI U QNGR. OYFXY NQQNDM GTIX YBR SCPPYY-FZGJL NQF, VY QNX VVLARW. NUJ VVL VBDM YFOTMYQ FHQ QUHLBRI. IAJ XND USYYE OYFXY TWUOGYQ YBR SCPPYY, MCF KUGMYE YIBP BVR UFNXR FHQ XUVI, "DRXMR, YBBXY OTSF FLR RUXNHTKOA TZ LTO. GMYL YBVSE LTO QTHG PHBB NUJ XVRY VX QBWNU RIEJ NUFH GMY ANWXJF." WJMFJ AENHAJX NSX FFCQ, "IIAY QBWLL IUQ. N EATQ JMCPM CF BIEYB ZTLR. GOG NZ V YIBP NUJ XVRY, GMYL BIHQX FYIC IIVSA VY. MB KUE NPR HIYQYPYYQ $10 IIYQUEX."'
eng_freq = [('a', 8.2), ('b', 1.5), ('c', 2.8), ('d', 4.3), ('e', 12.7), ('f', 2.2), ('g', 2), ('h', 6.1), ('i', 7), ('j', 0.2), ('k', 0.8), ('l', 4), ('m', 2.4), ('n', 6.8), ('o', 7.5), ('p', 1.9), ('q', 0.1), ('r', 6), ('s', 6.3), ('t', 9.1), ('u', 2.8), ('v', 1), ('w', 2.4), ('x', 0.2), ('y', 2), ('z', 0.1)]
 
ascii = ''.join([chr(x) for x in range(2**8)])

class Message(str):
  def __new__(cls, message, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
      return str.__new__(cls,str(message))

  def __init__(self, message, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
      if isinstance(message,Message):alphabet = message.alphabet
      self.alphabet = alphabet
      self.modulus = len(alphabet)
      self.string = str(self)
      self.string_locations = {}
      if message == '':
          self.m2n = 0
      else:
          self.number = self.m2n()

  def __repr__(self):
      return '*{}*'.format(self.string)

  def __getslice__(self,i,j):
      return Message(str.__getslice__(self,i,j),self.alphabet)

  def __getitem__(self,index):
      return Message(str.__getitem__(self,index),self.alphabet)

  def __eq__(self,other):
      try:
        return (self.alphabet == other.alphabet) and (str(self) == str(other))
      except AttributeError: return False
     
  def __add__(self,other):
      return(Message(str(self) + str(other),self.alphabet))
    
  def capitalize(self):
      return Message(str(self).capitalize(),self.alphabet)

  def center(self,width,fillchar=' '):
      return Message(str(self).center(width,fillchar),self.alphabet)

  def ljust(self,width,fillchar=' '):
      return Message(str(self).ljust(width,fillchar),self.alphabet)

  def expandtabs(self,tabsize = 8):
      return Message(str(self).expandtabs(tabsize),self.alphabet)

  def join(self):
      raise ValueError('messages cannot be joined')
  
  def lower(self):
      return Message(str(self).lower(),self.alphabet)

  def lstrip(self,chars = None):
      return Message(str(self).lstrip(chars),self.alphabet)

  def replace(self,old,new,count=None):
      if count == None: count = self.count(old)
      return Message(str(self).replace(old,new,count),self.alphabet)

  def swapcase(self):
      return Message(str(self).swapcase(),self.alphabet)

  def zfill(self,width):
      return Message(str(self).zfill(width),self.alphabet)

  def title(self):
      return Message(str(self).title(),self.alphabet)

  def upper(self):
      return Message(str(self).upper(),self.alphabet)

  def find_all(self,sub,start=0):
      count = 0
      F = 0
      while self.find(sub,start) != -1:
        count += 1
        start += len(sub)
      return count       

  def change_alphabet(self,alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
      self.alphabet = alphabet
      self.modulus = len(alphabet)
      return alphabet

  def good(self):
      """
     returns True if every character in the message is in the alphabet.  Otherwise
     returns a list of all characters not in the alphabet.
      """
      bad = []
      for x in self:
        if self.alphabet.rfind(x) == -1: bad = bad + [x]
      if len(bad) == 0: return True
      return badm2n

  def strip(self):
      """
  removes all characters not in alphabet.
      """
      strippedtext = ''
      for x in self:
          if self.alphabet.find(x)>-1:
            strippedtext=''.join([strippedtext,x])
      return Message(strippedtext,self.alphabet)

  def substitute(self,newalphabet='ZYXWVUTSRQPONMLKJIHGFEDCBA'):
      """
 Substitutes each alphabet character with corresponding letter in new alphabet.
 Default switches order of standard alphabet.
      """   
      alphabet = self.alphabet
      return Message( ''.join([newalphabet[alphabet.index(char)]
                        if char in alphabet else char
                        for char in self]),newalphabet)    

  def message_to_number(self):
      '''Each character in the string is replaced by it's ascii 2-hexdigit code.
  The resulting long string is interrupted as an hexadeciaml number and returned as an integer.
  '''
      return int(self.string.encode('hex'),16)

  m2n = message_to_number

  def to_letters(self, numbers):
      """
      the nth character in return string is the numbers[n] letter in alphabet.
      """
      return ''.join(self.alphabet[numbers[i]] for i in range(len(numbers)))

  def to_integers(self):
      """
      Returns list of integer value for each character in text.
      """
      a=self.alphabet
      l = []
      for x in self:
          if x in a:
            l += [a.find(x) ]
          else:
            l += [x]
      return l
    
  def intstring(self,n):
    '''Returns a string with 2-digit index in self.alphabet of each letter
in self.  there will be a space between each integer.  Consequently, you might not want this function if the alphabet
is more than 100 characters.  But it's good for classical ciphers.
'''
    L = ''
    for z in self:
        if z in self.alphabet: 
            L += '{:0{}d} '.format(self.alphabet.index(z),n)
        else: L += z
    return L
  
  def smoosh(self,n=5):
      """
      Strips the message of all characters not in the alphabet, inlcuding spaces, then
      separates the message into words of equal length = n
      """
      temp = self.strip()
      if n > 0:
        d,r = divmod(len(temp),n)
        sm = [ temp[n*i:n*(i+1)] for i in xrange(d) ]
        if r > 0: sm.append(temp[-r:])
        return Message(' '.join(sm))
      else:
        return temp


  def boxed(self,cols = 20):
      rows, remainder = divmod(len(self),cols)
      if remainder > 0: rows += 1
      return Message('\n'.join( [ '\t'.join( [char for char in row])
                                  for row in [self[cols*i:cols*(i+1)]
                                      for i in xrange(rows)] ] ), self.alphabet)
                     
  def unboxed(self):
      return self.replace('\t','').replace('\n','')


  def grouping(self,n):
      '''groups message into groups of n character each. Returns a new message.
'''
      return Message(' '.join([self[i:i+n] for i in range(0,len(self),n)
                               ]) )


  def to_integerstring(self,n):
      """
      Returns string of n-digit integer for each character in text.
      """
      return ''.join(
        ['{:0{}d}'.format(z,n) for z in self.to_integers() ])

  def frequencies(self,sortby= 0):
    alphabet = self.alphabet
    total = len(self)
    freq = [ ( x,round(float(self.count(x)) / total ,3) ) for x in alphabet]
    freq.sort(key=lambda x: x[sortby])
    return freq

  def shift_test(self,shifts=20):
    '''
Counts the number of coincidences in the text for each shift
    '''
    l = len(self)
    tests = [0]
    for shift in range(1,shifts):
      tests += [float(len([ x for x in range(l-shift) if self[x+shift]==self[x] ]))]
    return tests

  def groups(self,number):
    l = len(self)
    lg = l / number
    groups = []
    for n in range(number):
      groups += [ Message(''.join( [ self[x] for x in range(l) if x%number == n ] )) ]
    return groups

  def shift_correlation(self,group_freq,eng_freq):
    m = self.modulus
    return [ (j, sum([ group_freq[i][1]*eng_freq[(i+j)%m][1] for i in range(m) ]) ) for j in range(m) ]

def number_to_message(number):
    '''Represents the number in base 16 and converts 2-digits to ascii code character.
An '0' is placed in front of the hexstring if otherwise it would have an odd number
of digits.
'''
    hexstring = hex(number)
    ndigits = len(hexstring)-2
    if hexstring[-1]=='L': ndigits -= 1
    hexstring = hexstring[2:2+ndigits]
    if ndigits%2 is not 0:
        hexstring = '0'+hexstring
        ndigits += 1
    return Message(''.join( [chr(int(hexstring[x:x+2],16)) for x in range(0,ndigits,2)] ),ascii)

n2m = number_to_message

#if __name__ == '__main__':
    
