# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 10:39:30 2016

@author: pnbrown
"""

#import numpy as np
import numpy.random as rnd
from atomic.classes import *

population = {}
population[0] = 333
population[0.5] = 333
population[1] = 334
#numPlayers = 1000
numActions = 3

players = []
initAction = 0
#testsens = 0
for sens in population :
    for player in range(0,population[sens]):
        players.append(Player(sensitivity=sens))
#for i in range(0,numPlayers) :
#    players.append(Player())

costs = []
costs.append(lambda x,s : (1+s)/200*x)
costs.append(lambda x,s : (1+s)/200*x + 1)
costs.append(lambda x,s : 2)

testG = Game(players,costs)


numIter = 10000
noChangeThresh = 100
noChange = 0

for i in range(0,numIter) :
    print(testG.currentActProf)
    lastAction = list(testG.currentActProf)
    player = rnd.choice(testG.players) # pick random player
    thiscost = player.currentCosts() # get costs
    minval = min(thiscost)
    ind = [j for j, v in enumerate(thiscost) if v == minval] # list of all min cost actions
    if player.currentAction not in ind :
        player.currentAction = rnd.choice(ind) # if the player isn't already playing one of his min cost actions, then switch to a random one
    testG.updateActions()
    if lastAction == testG.currentActProf :
        noChange += 1
    else :
        noChange = 0
    if noChange > noChangeThresh :
        break