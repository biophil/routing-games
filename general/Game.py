# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:14:27 2016

@author: pnbrown
"""

import gradient
import numpy as np
import numpy.linalg as npla
from collections import defaultdict, OrderedDict

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
        
    def cost(self,flowOnEdges,sensitivity=1) :
        cost = 0
        for edge in self.edges :
            if edge in flowOnEdges :
                cost += edge.cost(flowOnEdges[edge],sensitivity)
            else :
                cost += edge.cost(0,sensitivity)
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
        self._state = OrderedDict()
        for path in self.paths :
            self._state[path] = 0
        self._state[self.paths[0]] = self.mass # put all flow on arbitrary path
        
    def getState(self) :
        return self._state
        
    def printState(self) :
        for path in self._state :
            print(path.getName() + ': ' + str(self._state[path]))
        
    def setState(self,newState) :
        for flow,path in zip(newState,self.paths) :
            self._state[path] = flow
            
    def _setAggState(self,aggState) : # this is a little bit dumb storing the whole aggState in each pop
        self._aggState = aggState
        
    def getAggState(self) :
        return self._aggState
    
    def _setCurrentCosts(self,game) :
        currentCosts = OrderedDict()
        aggFlowOnEdges = game.getFlowOnEdges()
        for path in self.paths :
            currentCosts[path] = path.cost(aggFlowOnEdges,self.sensitivity)
        self._currentCosts = currentCosts
        return self._currentCosts
        
    def getCurrentCosts(self,game,update=False) :
        if update :
            return self._setCurrentCosts(game)
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
            self._popState = OrderedDict()
            for pop in self.populations :
                pop.initState()
                self._popState[pop] = pop.getState()
        else :
            self._popState = populationState
        self._aggState = OrderedDict()
        self._setAggregateState()
        for pop in self.populations :
            pop._setCurrentCosts(self)
        
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
        
    def getFlowOnEdges(self) :
        # takes aggregate state and returns dict of edge:flow key:value pairs
#        aggState = self._aggState
        flowOnEdges = defaultdict(float)
        for path in self._aggState :
            for edge in path.edges :
                flowOnEdges[edge] += self._aggState[path]
        return flowOnEdges
        
    # I THINK THIS IS THE PROBLEM: I'M STORING ALL THE STUFF IN DICTS, AND WHEN I PULL VALUES() OUT IT RE-ORDERS THEM
    # THAT'S PROBABLY NOT THE PROBLEM. I DON'T KNOW WHAT ELSE IS GOING ON, BUT SOMETHING ISN'T RIGHT. 
    def learn(self,stepsize=0.1,reltol=1e-6,maxit=100,verbose=True) :
        numit = 0
        while True :
            tol = -1
            if numit<=maxit :
                for pop in self.populations :
                    self._setAggregateState()
                    popflow = pop.getState()
                    popflowList = list(popflow.values())
                    popCosts = pop.getCurrentCosts(self,update=True)
                    popCostsList = list(popCosts.values())
                    print('\n'+pop.name)
                    dispFlow = [(key.getName(),value) for key,value in popflow.items()]
                    dispCost = [(key.getName(),value) for key,value in popCosts.items()]
                    print('pop flow: ' + str(dispFlow))
                    print('pop cost: ' + str(dispCost))
                    nextFlow = gradient.safeStep(popflowList,popCostsList,stepsize)
                    nextFlow = np.reshape(nextFlow,len(popflowList))
                    print('next flow: ' + str(nextFlow))
                    # compute norm difference here:
                    diff = np.reshape(popflowList,[len(popflowList)])-nextFlow
                    tol = max([tol,abs(npla.norm(diff))])
                    pop.setState(nextFlow)
                if tol<reltol :
                    print('Min tolerance achieved; hopefully it worked. tol = ' + str(tol))
                    print('Number of iterations: ' + str(numit))
                    break
#                print("aggregate state: " + str(self.getAggregateState(update=True)))
            else :
                print('Max iterations exceeded; sorry dude.')
                print('Number of iterations: ' + str(numit))
                break
            numit += 1
        print(self.getAggregateState())