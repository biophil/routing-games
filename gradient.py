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
    return [i for i,f in enumerate(flow) if f[0] > ZERO]
    
    
def safeStep(flow,payoffs,stepsize) :
    n = len(payoffs)
    payoffsShaped = np.reshape(payoffs,[n,1])
    lastFlow = np.reshape(flow,[n,1])
    posIndices = getNonZeroIndices(lastFlow)
    if len(posIndices) < 2 : # we're done
#        print('less than 2 pos indices:' + str(posIndices))
        return lastFlow
    else :
#        print('pos indices:' + str(posIndices))
        payoffsReduced = np.zeros(len(posIndices))
        for i,idx in enumerate(posIndices) :
            payoffsReduced[i] = (payoffsShaped[idx][0])
        gradReduced = gradient(payoffsReduced)
        grad = np.zeros([n,1])
        for idx, g in enumerate(gradReduced) :
            grad[posIndices[idx]] = g
#        return grad
#        thisStep = stepsize*grad
        gradStep = stepsize*grad
        nextFlow = gradStep + lastFlow
        if np.min(nextFlow) > -ZERO :
            return nextFlow
        else : # recurse thru with partial steps
#            print(nextFlow)
            badIdx, overshoot = min(enumerate(nextFlow), key=itemgetter(1))
            overshoot = overshoot[0]
#            print(badIdx)
#            print(lastFlow)
#            print(grad)
            partialStep = -lastFlow[badIdx][0]/grad[badIdx][0] # amount of step that takes us to 0
            remainingStep = stepsize - partialStep # still need to take this step
            partialGradStep = grad*partialStep
            nextFlow = partialGradStep + lastFlow # this takes us to zero
#            print(badIdx,overshoot)
#            print(partialGradStep,partialStep,grad)
            return safeStep(nextFlow,payoffs,remainingStep)
        # here's the ideal: you 