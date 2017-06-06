#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 17:40:26 2017

@author: pnbrown
"""
import scipy.optimize as opt
import numpy as np
import matplotlib.pyplot as plt


def Ktwo(kone,SL,SU) :
    return max(0,(kone*kone*SL*SU-1)/(SL+SU+2*kone*SL*SU))

def Kone(T,SL,SU,a,b) :
    func = lambda k,SL,SU : a*k + b*Ktwo(k,SL,SU) - T
    return opt.fsolve(func,0,(SL,SU))[0]

def kk(T,SL,SU,a,b) : # this seems to check out, FWIW
    kone = Kone(T,SL,SU,a,b)
    return kone,Ktwo(kone,SL,SU)

def PoA(T,SL,SU,a,b) :
    kone,ktwo = kk(T,SL,SU,a,b)
    gmtoll = 1/np.sqrt(SL*SU)
    if kone < gmtoll :
        return 4/3*(1-kone*SL/(1+kone*SL)**2)
    else :
        return 4/3*(1-(1+kone*SL)*(SL/SU+kone*SL)/(1+2*kone*SL+SL/SU)**2)
    
sGM = 1
qq = [1/2,1/10,1/100,1/1000]
Tmax = 8
TT = np.array(range(0,1001))/1000*Tmax
abar = 1
bbar = 1

PoAs = {}

for q in qq :
    PoAs[q] = np.zeros(len(TT))
    sL = np.sqrt(q)
    sU = np.sqrt(1/q)
    for idx,T in enumerate(TT) :
        PoAs[q][idx] = PoA(T,sL,sU,abar,bbar)

ax = plt.subplot(111)
lines = {}
for q in qq :
    lines[q] = plt.plot(TT,PoAs[q])
    
for line in lines:
    lines[line][0].set_linewidth(6)



#ax = plt.subplot(111, xlabel='x', ylabel='y', title='title')
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(20)