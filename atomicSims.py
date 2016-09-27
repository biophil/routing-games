# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 10:39:30 2016

@author: pnbrown
"""

#import numpy as np
import numpy.random as rnd
from atomic.classes import *

population = {}
population[0.1] = 333
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
#costs.append(lambda x,s : (1+s)/200*x)     # mc toll
#costs.append(lambda x,s : (1+s)/200*x + 1) # mc toll
#costs.append(lambda x,s : 2)
costs.append(lambda x,s : x/200 + s*10)        # fixed toll of tau_1 = 10
costs.append(lambda x,s : x/200 + 1 + s*5)# fixed toll of tau_2 = 5
costs.append(lambda x,s : 2)

testG = Game(players,costs)


numIter = 10000
noChangeThresh = 10000
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
    
players_actions = {0:[], 1:[], 2:[]}
for player in testG.players :
    players_actions[player.currentAction].append(player.sensitivity)
print('types on path 0 :' + str(set(players_actions[0])))
print('types on path 1 :' + str(set(players_actions[1])))
print('types on path 2 :' + str(set(players_actions[2])))
