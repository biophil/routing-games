# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 16:16:08 2016

@author: pnbrown
"""

import numpy as np
from operator import itemgetter

ZERO = 1e-12

def gradient(payoffs) :
    n = len(payoffs)
    Phi = np.eye(n)-1/n*np.ones([n,n]) # project into tangent space
    payoffs = np.reshape(payoffs,[n,1])
    return np.reshape(-Phi@payoffs,n)
    
def getNonZeroIndices(flow) :
    return [i for i,f in enumerate(flow) if f > ZERO]
    
def getZeroIndices(flow) :
    return [i for i,f in enumerate(flow) if f <= ZERO]
    
def getAcceptableIndices(flow,grad) :
    # get indices where either flow or gradient are nonnegative
    return [i for i,j in enumerate(zip(flow,grad)) if j[0]>ZERO or j[1]>=0] 
    
    
def safeStep(flow,payoffs,stepsize) :
    n = len(payoffs)
    payoffsShaped = np.reshape(payoffs,n)
    lastFlow = np.reshape(flow,n)
    grad = gradient(payoffsShaped)
    goodIndices = getAcceptableIndices(lastFlow,grad)
    if len(goodIndices) < 2 : # we're done
#        print('less than 2 pos indices:' + str(posIndices))
        return lastFlow
    else :
#        print('pos indices:' + str(posIndices))
        payoffsReduced = np.zeros(len(goodIndices))
        for i,idx in enumerate(goodIndices) :
            payoffsReduced[i] = (payoffsShaped[idx])
        gradReduced = gradient(payoffsReduced)
        grad = np.zeros(n)
        for idx, g in enumerate(gradReduced) :
            grad[goodIndices[idx]] = g
    #        return grad
    #        thisStep = stepsize*grad
        gradStep = stepsize*grad
        nextFlow = gradStep + lastFlow
        if np.min(nextFlow) > -ZERO :
            return nextFlow
        else : # recurse thru with partial steps
    #            print(nextFlow)
            badIdx, overshoot = min(enumerate(nextFlow), key=itemgetter(1))
    #            overshoot = overshoot
    #            print(badIdx)
    #            print(lastFlow)
    #            print(grad)
            partialStep = -lastFlow[badIdx]/grad[badIdx] # amount of step that takes us to 0
            remainingStep = stepsize - partialStep # still need to take this step
            partialGradStep = grad*partialStep
            nextFlow = partialGradStep + lastFlow # this takes us to zero
    #            print(badIdx,overshoot)
    #            print(partialGradStep,partialStep,grad)
            return safeStep(nextFlow,payoffs,remainingStep)