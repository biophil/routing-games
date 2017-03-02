#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 11:48:37 2017

@author: pnbrown
"""

import linear as lin
import numpy as np
import numpy.linalg as la
import numpy.random as rnd

# approach: build a random network, specify a pile of r's, and start stepping up the r's until fL uses all links.
# on each setting, check each hetero vertex to see if it's worse than the worst of the homog vertices
# if we ever find one, stick it in a list of bad ones

badNets = []

rr = np.array(range(1,100))/10

class BreakIt(Exception) :
    pass

gl = 0.2
gu = 3
#gu = 7/3 # homog poa of .2 is same as 7/3
#gu = 1/gl
zL = 1/(1+gl)
zU = 1/(1+gu)

#zL = 1
#zU = 0

rnd.seed(1)

numNets = 1

break_the_loop = False

def PoAL(gamma) :
    return 1/((1+gamma) - 1/4*(1+gamma)**2)
    
def PoAU(gamma) :
    return (1+gamma)**2/4/gamma
    
def PoAHom(gamma) :
    if gamma <= 1 :
        return PoAL(gamma)
    else :
        return PoAU(gamma)

def check3linkbadness(net,zL,zU) :
    LL = net.Lz([zL]*2)
    LU = net.Lz([zU]*2)
    Lhet = net.Lz([zL,zU])
    Lopt = net.Lz([.5,5])
    print('homog L tot lat: '+str(LL))
    print('homog U tot lat: '+str(LU))
    print('heterog tot lat: '+str(Lhet))
    print('PoAL: ' + str(LL/Lopt))
    print('PoAh: ' + str(Lhet/Lopt))
    
    if Lhet > max(LL,LU) :
        print('HETERO IS WORSE!')

for i in range(numNets) :
    print('checking net number ' + str(i))
    n = 3
    a = rnd.rand(n)
    b = 2*rnd.rand(n)
    b.sort()
    net = lin.Parallel(a,b)
    for r in rr :
        net.r = r
        fL = net.fz([zL]*(net.n-1))
        if fL[-1] == 0 : # i.e., if network isn't fully-utilized
            LL = net.L(fL)
            LU = net.Lz([zU]*(net.n-1))
            for j in range(1,net.n-1) : # check each heterog vertex
                zz = [zL]*j + [zU] * (net.n-1-j)
#                print(zz)
                assert(len(zz) == net.n-1)
                Lhet = net.Lz(zz)
                if Lhet > max(LL,LU) :
                    Lopt = net.Lz([.5]*(net.n-1))
                    badNets.append({'net':net})
                    badNets[-1]['z'] = zz
                    badNets[-1]['poa'] = Lhet/Lopt
                    break_the_loop = True
                    print('BAD NETWORK FOUND! network number ' + str(i))
                    break
            if break_the_loop :
                break # this is a silly hack to break the 2 inner loops but not the outer. I should switch to using a return!