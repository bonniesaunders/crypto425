from DES_simplified import *

m,c = 377, 123
m2,c2 = 'This is a test of double DES','000101100010100111011100001110000010101100101110000101101111001110000010101100101110000101101111110001001001000101101111001000111101110101110011101100101110001000111101000101101111010000010101001011001110000101101111111100111001010000010101011111000101100101100000111101011001110101110011000101101111000100100000100110101000001011100000'

def MIMA(m,c,key1 = range(2**9),key2 = range(2**9)):
    '''
    Man in the Middle Attack on Double DES'.
    m and c are paired message and coded message.
    key1 is a possible range of key values for the first DES.
    key2 is a possible range of key values for the second DES.
    If key1, key2 is not unique, run MIMA again with different m,c and
    reduced ranges.
    
    '''
    setone = {}
    k1,k2 = [],[]
    for k in key1:
        K = Key(k)
        setone[DESint(m).enc(K)] = k
    for k in key2:
        K = Key(k)
        DC = DESint(c).dec(K)
        if DC in setone:
            k1 += [setone[DC]]
            k2 += [k]
    return k1,k2

def TWODES12(input,K1,K2,rounds=4):
    '''
    Performs double DES on a message string.  Each character is a block of 12 bits
    Encrypts any character string by converting each character in the string to a 12 bit DESint
    '''
    out = ''
    for char in input:
        out += str(DESint(ord(char)).enc(K1,rounds).enc(K2,rounds) )
    return out

def TWODES12_d(output,K1,K2,rounds=4):
    '''
    Decrypts the TWODES12
    Decrypts a string of bits, 12 bits at a time
    '''
    decrypted = ''
    nbits = len(output)
    for n in range(0,nbits,12):
        I = DESint(int(output[n:n+12],2))
        decrypted += chr( I.dec(K2,rounds).dec(K1,rounds) )
    return decrypted
