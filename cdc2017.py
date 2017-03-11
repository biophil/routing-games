#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 15:08:01 2017

@author: pnbrown
"""

import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

def PoAL(gamma) :
    return 1/((1+gamma) - 1/4*(1+gamma)**2)
    
def PoAU(gamma) :
    return (1+gamma)**2/4/gamma
    
def PoAHom(gamma) :
    if gamma <= 1 :
        return PoAL(gamma)
    else :
        return PoAU(gamma)

def PoAGM(q) :
    return 4/3*(1-np.sqrt(q)/(1+np.sqrt(q))**2)

def getqq(numpoints) :
    return np.array(range(numpoints))/(numpoints-1)

def plotWRNA(numpoints,label='') :
    qq = getqq(numpoints)
    return plt.plot(qq,[PoAHom(q) for q in qq],label=label)

def plotGM(numpoints,label='') :
    qq = getqq(numpoints)
    return plt.plot(qq,[PoAGM(q) for q in qq],label=label)
    
def plotAGG(numpoints,label='') :
    qq = getqq(numpoints)[1:]
    return plt.plot(qq,[PoAU(np.sqrt(1/q)) for q in qq],label=label)


plt.figure(10)
plt.clf()
wrna, = plotWRNA(100,label='WRNA')
gm, = plotGM(100,label='GM')
agg, = plotAGG(100,label='AGG')
plt.legend(handles=[wrna,gm,agg])
plt.axis([0, 1, 1, 2])