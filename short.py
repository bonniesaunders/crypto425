from matmodtest import *

n = 2819652760422015729904892439807232547685748784246846443629119262186885440649211743087974428406479
e = 65537
c = 1403461135086510666860337237136727557445325927236744361020674130487147714593168081069841540976587 |mod| n

def short(c,n,e,power):

    first = { c*((x|mod|n)**(-e)):x for x in xrange(1,power+1)}
    print 'first done'
    for y in xrange(1,power+1):
        x = first.get( (y|mod|n)**e )
        if x is not None: return x*y
    return 'failed'
