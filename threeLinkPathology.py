# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:27:42 2016

@author: pnbrown
"""

#import numpy as np
#import numpy.linalg as npla
#import scipy.linalg as spla
#import gradient
import general.Game as gm
from gradient import gradientSelect


# initializes my 3-link asymmetric pathology

e1 = gm.Edge(lambda x:x+1,name='e1')
e1.setToll(lambda x:x)
e2 = gm.Edge(lambda x:x,name='e2')
e2.setToll(lambda x:x)
e3 = gm.Edge(lambda x:1,name='e3')
p1 = gm.Path([e1],name='p1')
p2 = gm.Path([e2],name='p2')
p3 = gm.Path([e3],name='p3')
pop1 = gm.Population([p1,p2],mass=0.5,sensitivity=1,name='upperPop')
pop2 = gm.Population([p2,p3],mass=1,sensitivity=0,name='lowerPop')
ThreeLink = gm.Game([e1,e2,e3],[p1,p2,p3],[pop1,pop2])

ThreeLink.populations[0].setState([0,.5])
ThreeLink.populations[1].setState([0,1])


    
gradientSelect([4,3,3,2],[1,2,3])