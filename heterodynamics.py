import numpy as np
import numpy.linalg as npla
import scipy.linalg as spla
import gradient

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