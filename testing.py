# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:29:40 2016

@author: pnbrown
"""


import general.Game as gm
import matplotlib.pyplot as plt
import gradient as gr
import numpy.random as rnd
import random
import farokhiHelpers as fh

#latencies = [(lambda x:x),(lambda x:1)]
#tolls = [(lambda x:x),(lambda x:0)]
#demands = [1]
#sensitivities = [1]
#pathsets = [[0,1]]
#
#Pigou = gm.SymmetricParallelNetwork(latencies,tolls,demands,sensitivities)

#edgeList = list(range(1,14))
#latencies = [(lambda x:x),
#             (lambda x:1),
#             (lambda x:2*x),
#             (lambda x:3),
#             (lambda x:x),
#             (lambda x:1),
#             (lambda x:2*x)]
#latencies = latencies*2
#latencies = latencies[0:-1]
#tolls = [(lambda x:0)]
#tolls = tolls*13
#demands = [1,2,3]
#sensitivities = [0,.5,1]
#
#
#Gtest = gm.FarokhiGame(edgeList,latencies,demands,sensitivities)
#
#Gtest.printGame()

#payoffs = [3.62,89,85,88,84]
#payoffs = [3.62,89,85,888,584]
#flow = [0,0,0,.85,.15]
#grad = gr.gradientSelect(payoffs,[])
#nextFlow = gr.safeStep(flow,payoffs,1)
#print(nextFlow)

massList = [2,1,.5]
rnd.seed(1)
G = fh.buildRandomNetworkDPR()
for idx,pop in enumerate(G.populations) : # set the population masses
    pop.mass = massList[idx]
    pop.initState()
G.totalMass = sum(massList)
fh.updateNetworkTollsDPR(G,1,fh.buildSMCDPR)
G._setAggregateState()

pop1 = G.populations[0]
pop2 = G.populations[1]
pop3 = G.populations[2]

fh.updateNetworkTollsDPR(G,1,fh.buildUniversalTollDPR)
G.setSensitivities([100,10,1])

#res = G.learn(stepsize=1,maxit=1000)

