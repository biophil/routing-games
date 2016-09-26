# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 10:50:43 2016

@author: pnbrown
"""

import numpy as np

class Player :
    game = None
    def __init__(self,sensitivity=0,currentAction=0) :
        self.sensitivity = sensitivity
        self.currentAction=currentAction
        
    def currentCosts(self) :
        if self.game is not None :
            costs = []
            for idx, costFunc in enumerate(self.game.costFunctions) :
                costs.append(costFunc(self.game.currentActProf[idx],self.sensitivity))
            return costs
        else :
            return None

class Game :
    def __init__(self,players,costFunctions) :
        # players is a list of Player() objects
        # costFunctions is a list of lambdas of the basic cost functions
        # each cost function is a lambda x,s : (1+s)*a*x + b
        self.costFunctions = costFunctions
        self.players = players
        self.numActions = len(costFunctions)
        self.currentActProf = list(np.zeros([self.numActions]))
        self.updateActions()
        for player in self.players :
            player.game = self
    
    def updateActions(self) :
        for action in range(0,self.numActions) :
            self.currentActProf[action] = self.aggFlow(self.players,action)
    
    def aggFlow(self,players,action) :
        # returns the number of players in players playing action
        numPlayers = 0
        for player in players :
            if player.currentAction == action :
                numPlayers += 1
        return numPlayers