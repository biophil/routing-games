# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 16:16:08 2016

@author: pnbrown
"""

import numpy as np
from operator import itemgetter

ZERO = 1e-12
SAFE_FRAC = .05

def gradient(payoffs) :
    n = len(payoffs)
    Phi = np.eye(n)-1/n*np.ones([n,n]) # project into tangent space
    payoffs = np.reshape(payoffs,[n,1])
    return np.reshape(-Phi@payoffs,n)

def gradientSelect(payoffs,badIndices) :
    n = len(payoffs)
    k = len(badIndices)
    Phi = np.eye(n)-1/(n-k)*np.ones([n,n])
    for badIdx in badIndices :
        Phi[badIdx,:] = np.zeros(n)
        Phi[:,badIdx] = np.zeros(n)
#        Phi[badIdx,badIdx] = 1
    payoffs = np.reshape(payoffs,[n,1])
    return np.reshape(-Phi@payoffs,n)

    
def getNonZeroIndices(flow) :
    return [i for i,f in enumerate(flow) if f > ZERO]
    
def getZeroIndices(flow) :
    return [i for i,f in enumerate(flow) if f <= ZERO]
    
def getAcceptableIndices(flow,grad) :
    # get indices where either flow or gradient are nonnegative
    return [i for i,j in enumerate(zip(flow,grad)) if j[0]>ZERO or j[1]>=0] 
    
def getBadIndices(flow,grad) :
    # get indices where either flow or gradient are nonpositive
    return [i for i,j in enumerate(zip(flow,grad)) if j[0]<=ZERO and j[1]<0] 
    
def pareDownPayoffs(flow,payoffs) :
    # program: loop over this:
    # 1. compute gradient
    # 2. run getAcceptableIndices()
    # 3. try again?
    localPayoffs = np.array(payoffs)
    localFlow = np.array(flow)
    done = False
    goodIndices = np.array(range(0,len(flow))) # start by assuming all are good
    while not done :
        grad = gradient(localPayoffs)
        newGoodIndices = getAcceptableIndices(localFlow,grad) # these are the new candidate good ones
        if len(goodIndices) == len(newGoodIndices) :
            break # didn't change, we're good to go
        # well, here's the thing: it might make more sense to pass
        # the "good indices" to gradient(). that way we do everything
        # more-or-less in place. Should be cleaner.
    return goodIndices
    
def safeStep(flow,payoffs,stepsize,autoAdjust=True) :
    n = len(payoffs)
    payoffsShaped = np.reshape(payoffs,n)
    lastFlow = np.reshape(flow,n)
    flowToCheck = lastFlow[:]
    badIndices = set()
    allIndices = set(range(0,n))
    while True :
        grad = gradientSelect(payoffsShaped,list(badIndices))
        newBadIndices = badIndices.union(set(getBadIndices(flowToCheck,grad)))
        if newBadIndices == badIndices :
            break
        if len(newBadIndices) > n-2 : # 
            return lastFlow
        badIndices = newBadIndices.copy()
#        print('pos indices:' + str(posIndices))
    goodIndices = list(allIndices - badIndices)
    payoffsReduced = np.zeros(len(goodIndices))
    for i,idx in enumerate(goodIndices) :
        payoffsReduced[i] = (payoffsShaped[idx])
    gradReduced = gradient(payoffsReduced)
    grad = np.zeros(n)
    for idx, g in enumerate(gradReduced) :
        grad[goodIndices[idx]] = g
#        return grad
#        thisStep = stepsize*grad
    autoStepsize = stepsize
    gradStep = autoStepsize*grad
    if autoAdjust :
        gradStep = gradStep/max(sum(flow),sum(abs(grad)))
        autoStepsize = autoStepsize/max(sum(flow),sum(abs(grad)))
#        if sum(abs(gradStep))>sum(flow)*SAFE_FRAC :
#            autoStepsize = stepsize * SAFE_FRAC*sum(flow)/sum(abs(gradStep))
#            gradStep = grad * autoStepsize
    nextFlow = gradStep + lastFlow
    if np.min(nextFlow) > -ZERO :
        return nextFlow
    else : # recurse thru with partial steps
#            print(nextFlow)
        remainingStep = autoStepsize
        while True : # loop here until we've backed up every neg index
            badIdx, overshoot = min(enumerate(nextFlow), key=itemgetter(1))
            if overshoot > -ZERO :
                break
            partialStep = -lastFlow[badIdx]/grad[badIdx] # amount of step that takes us to 0
            remainingStep = remainingStep - partialStep # still need to take this step
            partialGradStep = grad*partialStep
            nextFlow = partialGradStep + lastFlow # this takes us to zero
            lastFlow = nextFlow[:]
        # we adjusted the stepsize in the recusion parent, so no need to do it again
        return safeStep(nextFlow,payoffs,remainingStep,autoAdjust=True) 