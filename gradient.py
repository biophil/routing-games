# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 16:16:08 2016

@author: pnbrown
"""

import numpy as np
from operator import itemgetter

ZERO = 1e-10

def gradient(payoffs) :
    n = len(payoffs)
    Phi = np.eye(n)-1/n*np.ones([n,n])
    payoffs = np.reshape(payoffs,[n,1])
    return -Phi@payoffs
    
def getNonZeroIndices(flow) :
    return [i for i,f in enumerate(flow) if f > ZERO]
    
    
def safeStep(flow,payoffs,stepsize) :
    safe = False
    n = len(payoffs)
    payoffsShaped = np.reshape(payoffs,[n,1])
    lastFlow = np.reshape(flow,[n,1])
    while not safe :
        grad = gradient(payoffsShaped)
#        thisStep = stepsize*grad
        gradStep = stepsize*grad
        nextFlow = gradStep + lastFlow
        if np.min(nextFlow) > -ZERO :
            return nextFlow
        else : # go right up to the bdry and send it to gradStep again
#            print(nextFlow)
            badIdx, overshoot = min(enumerate(nextFlow), key=itemgetter(1))
            overshoot = overshoot[0]
            partialStep = -lastFlow[0][badIdx]/grad[0][badIdx] # amount of step that takes us to 0
            remainingStep = stepsize - partialStep # still need to take this step
            partialGradStep = grad*partialStep
            nextFlow = partialGradStep + lastFlow # this takes us to zero
#            print(badIdx,overshoot)
#            print(partialGradStep,partialStep,grad)
            return nextFlow
        # here's the ideal: you 