# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:14:27 2016

@author: pnbrown
"""

import gradient
import numpy as np
import numpy.linalg as npla

class Edge :
    
    def __init__(self,latency,toll=(lambda x: 0),name='') :
        # latency is a lambda of nominal latency function
        # toll is either None or a lambda of tolling function
        self._latency = latency
        self._toll = toll
        self._name = name
        
    def cost(self,flow,sensitivity=1) :
        return self._latency(flow) + sensitivity*self._toll(flow)
        
    def latency(self,flow) :
        return self._latency(flow)
        
    def toll(self,flow) :
        return self._toll(flow)
        
    def setToll(self,toll) :
        self._toll = toll
        
    def setLatency(self,latency) :
        self._latency = latency
        
    def setName(self,name) :
        self._name = name
        
    def getName(self) :
        return self._name
        
class Path :
    
    def __init__(self,*edges,name='') :
        self.edges = edges
        self._name = name
        
    def cost(self,flow,sensitivity=1) :
        cost = 0
        for edge in self.edges :
            cost += edge.cost(flow,sensitivity)
        return cost
        
    def latency(self,flow) :
        return self.cost(flow,sensitivity=0)
        
    def display(self) :
        return [e.getName() for e in self.edges]
        
    def setName(self,name) :
        self._name = name
        
    def getName(self) :
        return self._name
        
#    def updatePopState(self,pop) :
#        self._popState[pop] = pop.
        
    

class Population :
    
    def __init__(self,paths,mass=1,sensitivity=1,name=''):
        self.paths = paths
        self.sensitivity = sensitivity
        self.mass = mass
        self._state = None
        self.numPaths = len(self.paths)
        self.name=name
        
    def initState(self) :
        self._state = {}
        for path in self.paths :
            self._state[path] = 0
        self._state[self.paths[0]] = self.mass # put all flow on arbitrary path
        
    def getState(self) :
        return self._state
        
    def setState(self,newState) :
        for idx,path in enumerate(self.paths) :
            self._state[path] = newState[idx]
            
    def _setAggState(self,aggState) :
        self._aggState = aggState
        
    def getAggState(self) :
        return self._aggState
    
    def _setCurrentCosts(self) :
        currentCosts = {}
        aggState = self.getAggState()
        for path in self.paths :
            currentCosts[path] = path.cost(aggState[path],self.sensitivity)
        self._currentCosts = currentCosts
        return self._currentCosts
        
    def getCurrentCosts(self,update=False) :
        if update :
            return self._setCurrentCosts()
        else :
            return self._currentCosts

class Game :
    
    def __init__(self,edges,paths,populations,populationState=None) :
        self.edges = tuple(edges)
        self.paths = tuple(paths)
        self.populations = tuple(populations)
        self.numPops = len(self.populations)
        self.numPaths = len(self.paths)
        self.totalMass = sum([pop.mass for pop in self.populations])
        
        if populationState is None : # initialize to something meaningless
            self._popState = {}
            for pop in self.populations :
                pop.initState()
                self._popState[pop] = pop.getState()
        else :
            self._popState = populationState
        self._aggState = {}
        self._setAggregateState()
        for pop in self.populations :
            pop._setCurrentCosts()
        
    def getPopState(self) :
        return self._popState
        
    def getAggregateState(self,update=False) :
        if update :
            return self._setAggregateState()
        else :
            return self._aggState
#            
        
    def _setAggregateState(self) :
        # sums population states to set aggregate state
        for path in self.paths :
            self._aggState[path] = 0
            for pop in self.populations :
                if path in pop.paths :
                    self._aggState[path] += pop._state[path]
        for pop in self.populations :
            pop._setAggState(self._aggState)
        return self._aggState
        
    # I THINK THIS IS THE PROBLEM: I'M STORING ALL THE STUFF IN DICTS, AND WHEN I PULL VALUES() OUT IT RE-ORDERS THEM
    def learn(self,stepsize=0.01,reltol=1e-6,maxit=100,verbose=True) :
        numit = 0
        while True :
            tol = -1
            if numit<=maxit :
                for pop in self.populations :
                    popflow = pop.getState()
                    popflowList = list(popflow.values())
                    popCosts = pop.getCurrentCosts(update=True)
                    popCostsList = list(popCosts.values())
                    print(pop.name)
                    print('pop flow: ' + str(popflowList))
                    print('pop cost: ' + str(popCostsList))
                    nextFlow = gradient.safeStep(popflowList,popCostsList,stepsize)
                    nextFlow = np.reshape(nextFlow,[len(popflowList)])
                    print(nextFlow)
                    # compute norm difference here:
                    diff = np.reshape(popflowList,[len(popflowList)])-nextFlow
                    tol = max([tol,abs(npla.norm(diff))])
                    pop.setState(nextFlow)
                if tol<reltol :
                    print('Min tolerance achieved; hopefully it worked. tol = ' + str(tol))
                    break
            else :
                print('Max iterations exceeded; sorry dude.')
                break
            numit += 1
        print(self.getPopState())