from ciphers425 import *

eng_freq.sort(key=lambda x:x[0])
A = [ x[1]/100. for x in eng_freq ]

def freq_print(freq,length=26):
    print ''.join(['{:1.3f} '.format(x) for x in freq[:length ] ])

def correlation(A,B,length=26):
    return sum( [ A[i]*B[i] for i in range(length) ])

def shift_correlation(A,B,j,length=26):
    return sum( [ A[i]*B[(i+j)%26] for i in range(length) ])
    
def shift(A,j):
    return [ A[(i+j)%26] for i in range(26) ]

