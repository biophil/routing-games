# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:29:40 2016

@author: pnbrown
"""


import general.Game as gm
import matplotlib.pyplot as plt

#latencies = [(lambda x:x),(lambda x:1)]
#tolls = [(lambda x:x),(lambda x:0)]
#demands = [1]
#sensitivities = [1]
#pathsets = [[0,1]]
#
#Pigou = gm.SymmetricParallelNetwork(latencies,tolls,demands,sensitivities)

edgeList = list(range(1,14))
latencies = [(lambda x:x),
             (lambda x:1),
             (lambda x:2*x),
             (lambda x:3),
             (lambda x:x),
             (lambda x:1),
             (lambda x:2*x)]
latencies = latencies*2
latencies = latencies[0:-1]
tolls = [(lambda x:0)]
tolls = tolls*13
demands = [1,2,3]
sensitivities = [0,.5,1]


Gtest = gm.FarokhiGame(edgeList,latencies,demands,sensitivities)

Gtest.printGame()