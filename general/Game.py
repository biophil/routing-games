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
        self.name = name
        
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
        return self.name
        
class Path :
    
    def __init__(self,edges,name='') :
        self.edges = edges
        self.name = name
        
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
        return self.name
        
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
        
    def printCosts(self) :
        for path in self._currentCosts :
            print(path.getName() + ': ' + str(self._currentCosts[path]))
        
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
            
    def atNashFlow(self,zero=1e-6) :
        # returns True if we're close to a Nash flow
        zeroFlowPathCosts = {path: self._currentCosts[path] for path in self.paths if self._state[path]<zero}
        otherPathCosts = {path: self._currentCosts[path] for path in self.paths if path not in zeroFlowPathCosts}
        minCost = min(self._currentCosts.values())
        for path in zeroFlowPathCosts : # ensure zero-flow have high costs
            if zeroFlowPathCosts[path]/minCost < 1 - zero :
                return False
        for path in otherPathCosts : # ensure pos-flow have low costs
            if otherPathCosts[path]/minCost > 1 + zero :
                return False
        return True

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
            pop._setCurrentCosts(self)
        return self._aggState
        
        
    def getFlowOnEdges(self,update=False) :
        # takes aggregate state and returns dict of edge:flow key:value pairs
#        aggState = self._aggState
        if update :
            self._setAggregateState()
        flowOnEdges = defaultdict(float)
        for path in self._aggState :
            for edge in path.edges :
#                print(self._aggState)
#                print(path.edges)
#                print(edge)
                flowOnEdges[edge] += self._aggState[path]
        return flowOnEdges
        
    def getTotalLatency(self,update=True) :
        flowOnEdges = self.getFlowOnEdges(update)
        totLat = 0.
        for edge in flowOnEdges :
            flow = flowOnEdges[edge]
            totLat += flow * edge.latency(flow)
        return totLat
        
    def printAggStateCosts(self) :
        self._setAggregateState()
        for pop in self.populations :
            print('')
            print(pop.name)
            pop._setCurrentCosts(self)
            for path in pop._currentCosts :
                toprint = path.getName() + ' flow: ' + str(pop._state[path])
                toprint += ',\t cost: ' + str(pop._currentCosts[path])
                print(toprint)
        
    def setZeroSensitivities(self) :
        self.setSensitivities([0]*len(self.populations))
            
    def setSensitivities(self,sensitivities) :
        for pop,sens in zip(self.populations,sensitivities) :
            pop.sensitivity = sens
            
    def atNashFlow(self,zero=1e-6) :
        # returns True if we're close to a Nash flow
        self._setAggregateState()
        for pop in self.populations :
            pop._setCurrentCosts(self)
            zeroFlowPathCosts = {path: pop._currentCosts[path] for path in pop.paths if pop._state[path]<zero}
            otherPathCosts = {path: pop._currentCosts[path] for path in pop.paths if path not in zeroFlowPathCosts}
            minCost = min(pop._currentCosts.values())
            for path in zeroFlowPathCosts : # ensure zero-flow have high costs
                if zeroFlowPathCosts[path]/minCost < 1 - zero :
                    return False
            for path in otherPathCosts : # ensure pos-flow have low costs
                if otherPathCosts[path]/minCost > 1 + zero :
                    return False
        return True

    def learn(self,stepsize=0.1,reltol=1e-6,maxit=100,verbose=False,veryVerbose=False) :
        # codes:
            # -1 = initialized
            #  1 = algo seems to have converged
            #  2 = max iter
        numit = 0
        totLat = []
        code = -1
        while True :
            tol = -1
            if numit<=maxit :
                for pop in self.populations :
#                    self._setAggregateState()
                    pop._setCurrentCosts(self)
                    if pop.atNashFlow(zero=reltol) :
                        pass
                    else :
                        popflow = pop.getState()
                        popflowList = list(popflow.values())
                        popCosts = pop.getCurrentCosts(self,update=True)
                        popCostsList = list(popCosts.values())
                        dispFlow = [(key.getName(),value) for key,value in popflow.items()]
                        dispCost = [(key.getName(),value) for key,value in popCosts.items()]
                        stepMod = pop.sensitivity*self.totalMass
                        nextFlow = gradient.safeStep(popflowList,popCostsList,stepsize/stepMod)
                        nextFlow = np.reshape(nextFlow,len(popflowList))
                        if veryVerbose :
                            print('\n'+pop.name)
                            print('pop flow: ' + str(dispFlow))
                            print('pop cost: ' + str(dispCost))
                            print('next flow: ' + str(nextFlow))
                        # compute norm difference here:
                        diff = np.reshape(popflowList,[len(popflowList)])-nextFlow
                        tol = max([tol,abs(npla.norm(diff))])
                        pop.setState(nextFlow)
                if self.atNashFlow(zero=reltol) :
                    if verbose :
                        print('Got to Nash flow; hopefully it worked. tol = ' + str(tol))
                        print('Number of iterations: ' + str(numit))
                    code = 1 # 
                    break
#                print("aggregate state: " + str(self.getAggregateState(update=True)))
            else :
                if verbose :
                    print('Max iterations exceeded; sorry dude.')
                    print('Number of iterations: ' + str(numit))
                code = 2
                break
            totLat.append(self.getTotalLatency())
            numit += 1
#        print(self.getAggregateState())
        if veryVerbose :
            self.printAggStateCosts()
        return totLat,code
        
    def printGame(self) :
        for pop in self.populations :
            print("\nPopulation " + pop.name + ":")
            for path in pop.paths :
                line = "path " + path.name + ", comprising edges "
                line += ' '.join(edge.name for edge in path.edges)
                print(line)
        
        
class ParallelNetwork(Game) :
    
    def __init__(self,latencies,tolls,demands,sensitivities,pathSets) :
        # for N edges and K populations
        # latencies: length-N iterable of lambdas of latency functions 
        # tolls: length-N iterable of lambdas of tolling functions 
        # demands: length-K iterable of r_k demand masses
        # sensitivities: length-K iterable of s_k sensitivity values
        # pathSets: length-K iterable of lists of accessible paths for each pop
        edges = []
        paths = []
        pops = []
        for idx,(latency,toll) in enumerate(zip(latencies,tolls)) :
            ename = 'e' + str(idx+1)
            pname = 'p' + str(idx+1)
            edge = Edge(latency,toll,ename)
            edges.append(edge)
            paths.append(Path([edge],name=pname))
        for idx,(demand,sensitivity,pathIndices) in enumerate(zip(demands,sensitivities,pathSets)) :
            popname = 'pop' + str(idx+1)
            pathList = []
            for idx in pathIndices :
                pathList.append(paths[idx])
            pops.append(Population(pathList,demand,sensitivity,popname))
        super().__init__(edges,paths,pops)
        
class SymmetricParallelNetwork(ParallelNetwork) :
    
    def __init__(self,latencies,tolls,demands,sensitivities) :
        pathSet = list(range(0,len(latencies)))
        pathSets = [pathSet]*len(demands)
        super().__init__(latencies,tolls,demands,sensitivities,pathSets)
        
class FarokhiGame(Game) :
    
    def __init__(self,edgeList,latencies,demandList=[1,1,1],sensitivityList=[1,1,1],tolls=None) :
        # CONVENTION: edgeList is 1-indexed
        edgeSet = set(edgeList)
        PotentialPaths = OrderedDict()
        PotentialPaths['pop1'] = []
        PotentialPaths['pop1'].append(set([1]))
        PotentialPaths['pop1'].append(set([2,3,4]))
        PotentialPaths['pop1'].append(set([2,7,8]))
        
        PotentialPaths['pop2'] = []
        PotentialPaths['pop2'].append(set([1,5,13]))
        PotentialPaths['pop2'].append(set([2,3,4,5,13]))
        PotentialPaths['pop2'].append(set([2,7,8,5,13]))
        PotentialPaths['pop2'].append(set([2,3,9,13]))
        PotentialPaths['pop2'].append(set([2,7,10,13]))
        
        PotentialPaths['pop3'] = []
        PotentialPaths['pop3'].append(set([11,6,3,4,5]))
        PotentialPaths['pop3'].append(set([11,6,3,9]))
        PotentialPaths['pop3'].append(set([11,6,7,8,5]))
        PotentialPaths['pop3'].append(set([11,6,7,10]))
        PotentialPaths['pop3'].append(set([11,12]))
        
        RealizedPaths = OrderedDict()
        for pop in PotentialPaths :
            RealizedPaths[pop] = [i for i in PotentialPaths[pop] if i <= edgeSet]
        
        # check if network is feasible
        tracker = 0
        for pop in RealizedPaths : 
            if len(RealizedPaths[pop]) == 0 :
                msg = "Population " + pop + " has no paths. Problem infeasible."
                raise NetworkDefinitionError(msg)
            else :
                tracker += len(RealizedPaths[pop])
        if tracker < 4:
            raise NetworkDefinitionError("All populations have exactly 1 path. Problem trivial.")
        edges = []
        if tolls is None :
            tolls = [lambda x : 0]*len(edgeList)
        paths = []
        pops = []
        for edgeIdx,latency,toll in zip(edgeList,latencies,tolls) :
            ename = 'e' + str(edgeIdx)
            edge = Edge(latency,toll,ename)
            edges.append(edge)
        for popName,demand,sens in zip(RealizedPaths,demandList,sensitivityList) :
            thesePaths = []
            for path in RealizedPaths[popName] :
                theseEdges = [edge for idx,edge in enumerate(edges) if edgeList[idx] in path] 
                pname = ''.join(edge.name for edge in theseEdges)
                thesePaths.append(Path(theseEdges,pname))
            pops.append(Population(thesePaths,demand,sens,popName))
            paths = paths + thesePaths
        super().__init__(edges,paths,pops)
        
class NetworkDefinitionError(Exception) :
    def __init__(self,message) :
        self.message = message