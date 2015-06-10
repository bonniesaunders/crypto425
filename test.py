from ciphers425 import *

def intstring(message):
    L = ''
#    print L
    for z in message:
        if z in message.alphabet: 
#            print z
            L += '%.2d '%(message.alphabet.index(z))
        else: L += z
    return L
