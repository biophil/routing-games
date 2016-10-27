# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:29:40 2016

@author: pnbrown
"""


import general.Game as gm

latencies = [(lambda x:x),(lambda x:1)]
tolls = [(lambda x:x),(lambda x:0)]
demands = [1]
sensitivities = [1]
pathsets = [[0,1]]

Pigou = gm.SymmetricParallelNetwork(latencies,tolls,demands,sensitivities)