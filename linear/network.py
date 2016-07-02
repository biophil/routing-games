# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 08:57:29 2016

@author: Philip
"""

from numpy import array, diag, zeros, ones, reshape
from numpy.linalg import solve

class Network:
    
    r = 1
    
    def __init__(self,A,b):
        # A is list-of-list or nxn array
        # b is list or array
        # initializes R and M via standard construction
        self.A = array(A)
        self.b = array(b)
        self.populate()
        
    def populate(self):
        self.b = reshape(self.b,[-1,1])
        self.n = self.b.size
        n = self.n
        self.X = zeros([n,n])
        for i in range(n-1):
            self.X[i,i:i+2] = [1,-1]
        self.Y = self.X[0:-1,:]
        self.Q = diag(reshape(-self.X@self.b,[-1]))
        self.Q = self.Q[:,0:-1]
        self.simplexCon = zeros([n,n])
        self.simplexCon[-1,:] = ones([1,n])
        self.P = self.X@self.A+self.simplexCon
        en = zeros([n,1])
        en[-1,0]=1
        self.R = solve(self.P,en)
        self.M = solve(self.P,self.Q)
        
    def fz(self,z):
        z = reshape(array(z),[-1,1])
        return self.r*self.R+self.M@z
        
    def costs(self,f,gamma):
        # f is column vector of path flows
        # gamma is real number; corresponds to mc-toll multiplier
        # outputs vector of path costs        
        return (1+gamma)*self.A@f+self.b
        
    def Lz(self,z):
        z = reshape(array(z),[-1,1])
        f = self.fz(z)
        return f.T@(self.A@f+self.b)
        
    def MTAM(self):
        return self.M.T@self.A@self.M
        
class twoPathGeneric(Network):
    # ae is length 3 list or array
    # This network:
    #     e3      e1
    # 0-------0--------0
    #         |        |
    #         |   e2   |
    #         |--------|
    # constructs A for this network

    def __init__(self,a,b):
        # ae is length 3 list or array
        # if len(b)=2, b is path-b's;
        # if len(b)=3, b is edge-b's
        self.A = diag(a[0:2])+a[2]*ones([2,2])
        if len(b) == 2: # case when b corresponds to path b's
            self.b = array(b)
        else :  # b corresponds to edge b's
            self.b = array([b[0:2]])+b[2]*ones(2)
        self.populate()
        
class threePathGeneric(Network):
    # This network: (different numbers from 6/17/16 p.3, but same net)
    #
    #                  e1
    #         | ----------------|
    #         |                 |
    #    e4   |   e2       e5   |
    # 0-------0--------0--------0
    # |                |
    # |      e3        |
    # |----------------|

    def __init__(self,a,b,permute=[0,1,2]):
        # ae is length 5 list or array
        # if len(b)=3, b is path-b's;
        # if len(b)=5, b is edge-b's
        m12 = zeros([3,3])
        m12[0:2,0:2] = ones([2,2])
        m23 = zeros([3,3])
        m23[1:3,1:3] = ones([2,2])
        self.A = diag(a[0:3])+a[3]*m12+a[4]*m23
        self.A = self.A[permute,:][:,permute]
        if len(b) == 3: # case when b corresponds to path b's
            self.b = array(b)
        else :  # b corresponds to edge b's
            self.b = array(b[0:3])+b[3]*m12[:0],+b[4]*m23[:1]
            self.b = self.b[permute]
        self.populate()
        
class fourPathGeneric1(Network):
    # This network: (different numbers from 6/17/16 p.6, but same net)
    #
    #                  e1
    #         | --------------------------------|
    #         |                e2               |
    #         |        |---------------|        |
    #    e5   |   e6   |   e3      e7  |   e8   |
    # 0-------0--------0-------0-------0--------0
    # |                        |
    # |      e4                |
    # |------------------------|

    def __init__(self,a,b,permute=[0,1,2,3]):
        # ae is length 5 list or array
        # if len(b)=4, b is path-b's;
        # if len(b)=8, b is edge-b's
        # note: permute is confusing, but to see path labels on above diagram,
        # just execute reshape(permute[permute]+1,[4,1])
        Ae5 = zeros([4,4])
        Ae5[0:3,0:3] = ones([3,3])
        Ae6 = zeros([4,4])
        Ae6[1:3,1:3] = ones([2,2])
        Ae7 = zeros([4,4])
        Ae7[2:4,2:4] = ones([2,2])
        Ae8 = zeros([4,4])
        Ae8[1:4,1:4] = ones([3,3])
        self.A = diag(a[0:4])+a[4]*Ae5+a[5]*Ae6+a[6]*Ae7+a[7]*Ae8
        self.A = self.A[permute,:][:,permute]
        if len(b) == 4: # case when b corresponds to path b's
            self.b = array(b)
        else :  # b corresponds to edge b's
            self.b = array(b[0:4])+b[4]*Ae5[:,0]+b[5]*Ae6[:,1]+b[6]*Ae7[:,2]+b[7]*Ae8[:,3]
            self.b = self.b[permute]
        self.populate()
        
        