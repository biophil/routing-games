
import dill
import pickle
import general.Game as gm
from general.Game import NetworkDefinitionError
import numpy.random as rnd
import random
import matplotlib.pyplot as plt


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
        
def totalVar(lst) :
    return sum([abs(lst[i]-lst[i-1]) for i in range(1,len(lst))])
        
def learnIt(game,startss=0.1,verb=False,rt=1e-6):
    code = 0
    LLtoret = []
    ss = startss
    ssdecay = 0.75
    ssgrowth = 1.1
    while code != 1 and len(LLtoret)<2e4:
        LL,code = game.learn(stepsize=ss,maxit=10,verbose=verb,reltol=rt)
        LLtoret += LL
        if verb:
            print('stepsize: ' + str(ss))
        if code == 2 :
            if totalVar(LL) > 1.1*abs(LL[-1]-LL[0]) :
                ss = ss*ssdecay
            else :
                LL,code = game.learn(stepsize=ss,maxit=1e3,verbose=verb,reltol=rt) # this one seems to work often enough
                LLtoret += LL
                if code == 2 :
                    ss = ss*ssgrowth
                if verb:
                    print('stepsize: ' + str(ss))
    return LLtoret,code
    
