# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 08:57:29 2016

@author: Philip
"""

from numpy import array, diag, zeros, ones, reshape
from numpy.linalg import solve, LinAlgError

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
        R,M = self._get_RM(self.A,self.b,self.n)
        self.R = R
        self.M = M
#        self.X = zeros([n,n])
#        for i in range(n-1):
#            self.X[i,i:i+2] = [1,-1]
#        self.Y = self.X[0:-1,:]
#        self.Q = diag(reshape(-self.X@self.b,[-1]))
#        self.Q = self.Q[:,0:-1]
#        self.simplexCon = zeros([n,n])
#        self.simplexCon[-1,:] = ones([1,n])
#        self.P = self.X@self.A+self.simplexCon
#        en = zeros([n,1])
#        en[-1,0]=1
#        try:
#            self.R = solve(self.P,en)
#            self.M = solve(self.P,self.Q)
#        except LinAlgError :
#            print('R and M not set, because you have a singular matrix')
#            self.R = None
#            self.M = None
            
    def _get_RM(self,A,b,n) :
        X = zeros([n,n])
        for i in range(n-1):
            X[i,i:i+2] = [1,-1]
        Y = X[0:-1,:]
        Q = diag(reshape(-X@b,[-1]))
        Q = Q[:,0:-1]
        simplexCon = zeros([n,n])
        simplexCon[-1,:] = ones([1,n])
        P = X@A+simplexCon
        en = zeros([n,1])
        en[-1,0]=1
        try:
            R = solve(P,en)
            M = solve(P,Q)
        except LinAlgError :
            print('R and M not set, because you have a singular matrix')
            R = None
            M = None
        return R,M
        
    def fz(self,z):
        z = reshape(array(z),[-1,1])
        return self.r*self.R+self.M@z
        
    def PoA(self,z) :
        Lopt = self.Lz(ones([self.n-1,1])/2)[0][0]
        Lz = self.Lz(z)[0][0]
        return Lz/Lopt
        
    def costs(self,f,gamma):
        # f is column vector of path flows
        # gamma is real number; corresponds to mc-toll multiplier
        # outputs vector of path costs        
        return (1+gamma)*self.A@f+self.b
        
    def Lz(self,z):
        z = reshape(array(z),[-1,1])
        f = self.fz(z)
        return self.L(f)
        
    def L(self,f) :
        # f is shape-[N,1] array of flows
        f = reshape(array(f),[-1,1])
        return (f.T@(self.A@f+self.b))[0][0]
        
    def MTAM(self):
        return self.M.T@self.A@self.M
        
        
class Parallel(Network) :
    def __init__(self,a,b) :
        # a is length-N list or array
        # b is length-N list or array
        self.A = diag(a)
        self.b = array(b)
        self.populate()
        self._lower_populate()
        
    def _lower_populate(self) :
        self.MM = []
        self.RR = []
        if self.n>2:
            for i in range(self.n-1,1,-1) :
                R,M = self._get_RM(self.A[0:i,0:i],self.b[0:i],i)
                sh = M.shape
                self.MM.append(zeros(self.M.shape))
                self.MM[-1][0:sh[0],0:sh[1]] = M
                self.RR.append(zeros(self.R.shape))
                self.RR[-1][0:sh[0]] = R
        
    def fz(self,z) :
        z = reshape(array(z),[-1,1])
        if len(z) == self.n-1 :
            f = self.r*self.R+self.M@z
            if any(x<0 for x in f) : # invalid flow; start working thru fewer-link flows
                for R,M in zip(self.RR,self.MM) :
#                    n = len(R)
#                    print(M)
#                    print(R)
#                    print(z[0:(n-1)])
                    fhere = self.r*R + M@z
                    if not any(x<0 for x in fhere) :
                        f = fhere
                        break # implicit: else loop again
            # finally, we may not have fixed it:
            if any(x<0 for x in f):
                f = zeros([self.n,1])
                f[0] = self.r
            return f
        else :
            raise IndexError('z is the wrong length; needs to be n-1')
        

        
class ParallelFixed(Parallel) :
    def __init__(self,a,b) :
        self.A = diag(a)
        self.b = array(b).reshape([-1,1])
        self.n = len(a)
        
    def ft(self,t) :
        # t is n-vector of tolls (or n-list)
        # this should be extremely slow because it instantiates a new net, but it seems to work
        t = array(t)
        t = t.reshape([-1,1])
        newconst = t+self.b
        idx = newconst[:,0].argsort(axis=0)
        fakeconst = newconst[idx] # sorted b + t
        tempNet = Parallel(self.A.diagonal()[idx],fakeconst)
        tempNet.r = self.r
        unorderedflow = tempNet.fz([1]*(self.n-1))
#        print(unorderedflow)
#        print(idx)
        flow = zeros([self.n,1])
        flow[idx] = unorderedflow
        return flow
        
        
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

    def __init__(self,a,b,permutation=[0,1,2]):
        # ae is length 5 list or array
        # if len(b)=3, b is path-b's;
        # if len(b)=5, b is edge-b's
        m12 = zeros([3,3])
        m12[0:2,0:2] = ones([2,2])
        m23 = zeros([3,3])
        m23[1:3,1:3] = ones([2,2])
        permute = array(permutation)
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
        
