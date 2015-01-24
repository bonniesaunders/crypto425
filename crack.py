"""
>>> alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
>>> CIPHERTEXT = 'YVCCFNFICU'
>>> crack_caesar(alphabet,CIPHERTEXT)
 0 yvccfnficu
 1 xubbemehbt
 2 wtaadldgas
 3 vszzckcfzr
 4 uryybjbeyq
 5 tqxxaiadxp
 6 spwwzhzcwo
 7 rovvygybvn
 8 qnuuxfxaum
 9 pmttwewztl
10 olssvdvysk
11 nkrrucuxrj
12 mjqqtbtwqi
13 lippsasvph
14 khoorzruog
15 jgnnqyqtnf
16 ifmmpxpsme
17 helloworld
18 gdkknvnqkc
19 fcjjmumpjb
20 ebiiltloia
21 dahhksknhz
22 czggjrjmgy
23 byffiqilfx
24 axeehphkew
25 zwddgogjdv
"""
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def crack_caesar(alphabet,ciphertext):
    """
    decrypts message -- which is provided in letters from alphabet--
    for each shift of the alphabet
    
    """
    print '\n'.joi
    n(['{:2} '.format(m)+''.join([alphabet[alphabet.index(letter)-m].lower()
              for letter in ciphertext]) for m in range(len(alphabet))])
    return
## What follows is a pedagogical activity for python: progressing from a double loop
## to a single line of join with list comprehension.
def crack_caesar1(alphabet,ciphertext):
    """
    first function, using nested loops
    """
    mod = len(alphabet)
    for j in range(mod):
        newtext=''
        for i in range(len(ciphertext)):
            newtext += alphabet[(alphabet.index(ciphertext[i])-j)%mod]
        print newtext.lower()
    return

def crack_caesar2(alphabet,ciphertext):
    """
    second function, replaces inside for-loop with list comprehension
    """
    mod = len(alphabet)
    newtext=''
    length = len(ciphertext)
    for j in range(mod):
        newtext = ''.join([alphabet[(alphabet.index(ciphertext[i])-j)%mod] for i in range(length)])
        print newtext.lower()
    return

def crack_caesar3(alphabet,ciphertext):
    """
    third function, replaces for-loop with list comprehension
    """
    A = alphabet.lower()
    mod = len(alphabet)
    length = len(ciphertext)
    tries = [''.join([alphabet[(alphabet.index(ciphertext[i])-j)%mod] for i in range(length)]) for j in range(len(A))]      
    for string in tries:
        print string.lower()
    return

def crack_caesar4(alphabet,ciphertext):
    """
    fourth function, combines print with list statement'MFQEFFAQZODKBF'
    """
    print '\n'.join([''.join([alphabet[alphabet.index(letter)-m]
              for letter in ciphertext]) for m,x in enumerate(alphabet)]).lower()
