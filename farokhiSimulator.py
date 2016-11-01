#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:52:03 2016

@author: pnbrown
"""

import general.Game as gm
from general.Game import NetworkDefinitionError
import numpy.random as rnd
import random
import matplotlib.pyplot as plt

# NOTE: I am not currently being careful with random seeds
rnd.seed(1)
numNetworksToCheck = 10
SL = 0.1
SU = 100
rL = 1/2
rM = 1
rH = 2

def randomLatencyDPR() :
    # needs to return a latency function of the form C + Af^4
    C = rnd.uniform()
    A = rnd.uniform()
    return lambda f : C + A*(f**4)

def buildUniversalTollDPR(lat,K) :
    # given latency function C + Af^4, builds appropriate universal toll
    C = lat(0)
    A = lat(1) - C
    return lambda f : K*(C+(5*A*(f**4)))
    
def buildSMCDPR(lat,K=1) :
    # given latency function C + Af^4, builds appropriate smc toll
    C = lat(0)
    A = lat(1) - C
    return lambda f : K*4*A*(f**4)
    
def updateNetworkTollsDPR(game,K,tollBuilder) :
    for edge in game.edges :
        edge.setToll(tollBuilder(edge._latency,K))

def buildRandomNetworkDPR() :
    numEdges = rnd.randint(8,14)
    edgeList = random.sample(range(1,14),numEdges)
    edgeList.sort()
    latencies = [randomLatencyDPR() for i in edgeList]
    try :
        return gm.FarokhiGame(edgeList,latencies)
    except NetworkDefinitionError as er :
        print('Invalid Network. Error: ' + str(er))
        return None
      
itr = 0
populationMasses = [[rL,rM,rH]]
#populationMasses.append([rL,rL,rL])
#populationMasses.append([rM,rM,rM])
#populationMasses.append([rH,rH,rH])
record = []
while itr < numNetworksToCheck :
    thisNet = buildRandomNetworkDPR()
    if thisNet is not None :
        itr += 1
        for massList in populationMasses :
            for idx,pop in enumerate(thisNet.populations) : # set the population masses
                pop.mass = massList[idx]
#                print(pop.mass)
                pop.initState()
            thisNet._setAggregateState()
            # first, need to find optimal flow for this population
            updateNetworkTollsDPR(thisNet,1,buildSMCDPR)
            thisNet.printGame()
            record.append({})
            record[-1]['net'] = thisNet
            record[-1]['popmass'] = massList
            LL,code = thisNet.learn(stepsize=0.01,maxit=1e6,verbose=False) # this one seems to work often enough
            if code == 2 :
                LL,code = thisNet.learn(stepsize=0.001,maxit=1e6) # try it with a tiny stepsize
                if code == 2 :
                    LL,code = thisNet.learn(stepsize=min(massList)/2,maxit=1e6) # try it with a huge stepsize
            if code == 1 :
                record[-1]['Lopt'] = LL[-1]
                record[-1]['num iter to opt'] = len(LL)
            else :
                record['opt did not converge'] = True
            
    