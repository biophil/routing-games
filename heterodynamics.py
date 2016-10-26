import numpy as np
import numpy.linalg as npla
import scipy.linalg as spla
import gradient
import general.Game as gm

A = np.array([[2,0,0],[0,1,0],[0,0,0]])
b = np.array([[0,1,2]]).T
P = np.concatenate((np.eye(3),np.eye(3),np.eye(3)),1)
gams = np.array([0.1,0.5,0.9])
Gam = np.diag([1+gams[0],1+gams[0],1+gams[0],1+gams[1],1+gams[1],1+gams[1],1+gams[2],1+gams[2],1+gams[2]])
PTAP = P.T@A@P
F = lambda xi : Gam@P.T@A@P@xi + P.T@b
Phibase = np.eye(3)-1/3*np.ones([3,3])
Phi = spla.block_diag(Phibase,Phibase,Phibase)

DFSymm = Gam@PTAP+PTAP@Gam

xitest = np.array([range(0,9)]).T

#f = gradient.safeStep([0,1,1],[2,1,.5],1)


e1 = gm.Edge(lambda x:x**2,name='e1')
e1.setToll(lambda x:2*x**2)
e2 = gm.Edge(lambda x:1,name='e2')
p1 = gm.Path(e1,name='p1')
p2 = gm.Path(e2,name='p2')
edges = (e1,e2)
paths = (p1,p2)
pop1 = gm.Population(paths,mass=0.5,sensitivity=0,name='pop1')
pop2 = gm.Population(paths,mass=0.5,sensitivity=1,name='pop2')
populations = (pop1,pop2)
Pigou = gm.Game(edges,paths,populations)



#Pigou.learn(maxit=1000)