# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 15:32:56 2016

@author: pnbrown
"""

import general.Game as gm
import matplotlib.pyplot as plt


# initializes my augmented Braess pathology

e1 = gm.Edge(lambda x:x,name='e1')
e1.setToll(lambda x:x)
e2 = gm.Edge(lambda x:1,name='e2')
e3 = gm.Edge(lambda x:1,name='e3')
e4 = gm.Edge(lambda x:x,name='e4')
e4.setToll(lambda x:x)
e5 = gm.Edge(lambda x:0,name='e5')
e6 = gm.Edge(lambda x:2.99,name='e6')
p1 = gm.Path([e1,e5,e4],name='p1')
p2 = gm.Path([e1,e2],name='p2')
p3 = gm.Path([e3,e4],name='p3')
p4 = gm.Path([e6],name='p4')
paths = [p1,p2,p3,p4]
pop1 = gm.Population(paths,mass=1,sensitivity=0,name='pop1')
pop2 = gm.Population(paths,mass=1,sensitivity=1,name='pop2')
AugBraess = gm.Game([e1,e2,e3,e4,e5,e6],paths,[pop1,pop2])

AugBraess.populations[0].setState([0,1,0,0])
AugBraess.populations[1].setState([0,0,1,0])

#AugBraess.learn()

