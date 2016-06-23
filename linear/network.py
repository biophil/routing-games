# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 08:57:29 2016

@author: Philip
"""

from numpy import array, diag, zeros, ones
from numpy.linalg import solve

class Network():
    
    
    def __init__(self,A,b):
        # A is list-of-list or nxn array
        # b is list or array
        self.A = array(A)
        self.b = array(b)
        self.n = self.b.size
        n = self.n
        self.X = zeros([n,n])
        for i in range(n-1):
            self.X[i,i:i+2] = [1,-1]
        self.Q = diag(-self.X@self.b)
        self.Q = self.Q[:,0:-1]
        self.simplexCon = zeros([n,n])
        self.simplexCon[-1,:] = ones([1,n])
        self.P = self.X@self.A+self.simplexCon
        en = zeros([n,1])
        en[-1,0]=1
        self.R = solve(self.P,en)
        self.M = solve(self.P,self.Q)